"""Core decompose pipeline — the single function that does everything."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from decompose.chunker import auto_chunk
from decompose.classifier import classify
from decompose.entities import extract_entities
from decompose.irreducibility import detect_irreducibility


@dataclass(slots=True)
class Unit:
    """A single semantic unit — the atomic output of decompose."""

    text: str
    authority: str
    risk: str
    content_type: str
    irreducible: bool
    attention: float
    actionable: bool
    entities: list[str]
    heading: str | None = None
    heading_path: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DecomposeResult:
    """Complete decompose output."""

    units: list[Unit]
    meta: dict = field(default_factory=dict)


def decompose_text(
    text: str,
    *,
    chunk_size: int = 2000,
    overlap: int = 200,
    compact: bool = False,
) -> dict:
    """Decompose text into classified semantic units.

    Args:
        text: Raw input text.
        chunk_size: Maximum characters per chunk.
        overlap: Character overlap between chunks.
        compact: If True, omit zero-value fields for smaller output.

    Returns:
        Dictionary with 'units' list and 'meta' summary.
    """
    start = time.monotonic()

    if not text or not text.strip():
        return {"units": [], "meta": {"total_units": 0, "error": "empty_input"}}

    MAX_INPUT = 10_000_000  # 10 MB
    if len(text) > MAX_INPUT:
        return {"units": [], "meta": {"total_units": 0, "error": "input_too_large", "max_bytes": MAX_INPUT}}

    chunk_size = max(100, min(chunk_size, 100_000))
    overlap = max(0, min(overlap, chunk_size // 2))

    # Chunk
    chunks = auto_chunk(text, chunk_size=chunk_size, overlap=overlap)

    # Classify + extract per chunk
    units: list[dict] = []
    all_standards: list[str] = []
    all_dates: list[str] = []
    authority_counts: dict[str, int] = {}
    risk_counts: dict[str, int] = {}

    for chunk in chunks:
        cls = classify(chunk.text)
        ents = extract_entities(chunk.text)
        irr = detect_irreducibility(chunk.text)

        all_standards.extend(ents.standards)
        all_dates.extend(ents.dates)
        authority_counts[cls.authority] = authority_counts.get(cls.authority, 0) + 1
        risk_counts[cls.risk] = risk_counts.get(cls.risk, 0) + 1

        # Build entity list (standards + references combined)
        entity_list = ents.standards + ents.references

        unit: dict = {
            "text": chunk.text,
            "authority": cls.authority,
            "risk": cls.risk,
            "type": cls.content_type,
            "irreducible": irr.irreducible,
            "attention": cls.attention,
        }

        if not compact:
            unit["actionable"] = cls.actionable
            unit["entities"] = entity_list
            unit["dates"] = ents.dates
            unit["financial"] = ents.financial
            unit["irreducibility"] = irr.recommendation
            if chunk.heading:
                unit["heading"] = chunk.heading
                unit["heading_path"] = chunk.heading_path
        else:
            # Compact: only include non-empty/non-default fields
            if cls.actionable:
                unit["actionable"] = True
            if entity_list:
                unit["entities"] = entity_list
            if ents.dates:
                unit["dates"] = ents.dates
            if ents.financial:
                unit["financial"] = ents.financial
            if irr.recommendation != "SUMMARIZABLE":
                unit["irreducibility"] = irr.recommendation
            if chunk.heading:
                unit["heading"] = chunk.heading

        units.append(unit)

    elapsed_ms = round((time.monotonic() - start) * 1000)

    # Token estimate: ~4 chars per token for English text
    input_tokens = len(text) // 4
    output_json = json.dumps(units, separators=(",", ":"))
    output_tokens = len(output_json) // 4
    reduction = round((1 - output_tokens / max(input_tokens, 1)) * 100) if input_tokens > 0 else 0

    return {
        "units": units,
        "meta": {
            "total_units": len(units),
            "input_chars": len(text),
            "processing_ms": elapsed_ms,
            "token_estimate": {"input": input_tokens, "output": output_tokens, "reduction_pct": max(0, reduction)},
            "authority_profile": authority_counts,
            "risk_profile": risk_counts,
            "standards_found": list(dict.fromkeys(all_standards)),
            "dates_found": list(dict.fromkeys(all_dates)),
            "_decompose": "0.2.0",
        },
    }


# Convenience alias
decompose = decompose_text


def filter_for_llm(
    result: dict,
    *,
    authorities: tuple[str, ...] = ("mandatory", "prohibitive", "directive", "conditional"),
    risks: tuple[str, ...] = ("safety_critical", "compliance", "financial", "contractual"),
    types: tuple[str, ...] = ("requirement", "constraint", "data", "definition"),
    min_attention: float = 0.0,
    include_headings: bool = True,
    max_tokens: int = 0,
) -> dict:
    """Filter decompose result to high-value units for LLM consumption.

    Takes the output of decompose_text() and returns only units that
    match the specified authority, risk, or content type criteria.
    Pattern proven in RBS Policy QC: Decompose as pre-filter before LLM
    extraction dramatically improves quality and reduces hallucination.

    Args:
        result: Output from decompose_text().
        authorities: Authority levels to keep.
        risks: Risk levels to keep.
        types: Content types to keep.
        min_attention: Minimum attention score (0.0 = no filter).
        include_headings: Prepend heading context to units.
        max_tokens: If > 0, truncate output to approx this many tokens.

    Returns:
        Dict with 'text' (filtered string), 'units' (filtered list),
        and 'meta' (input_units, output_units, reduction_pct, token_estimate).
    """
    units = result.get("units", [])
    if not units:
        return {
            "text": "",
            "units": [],
            "meta": {"input_units": 0, "output_units": 0, "reduction_pct": 0, "token_estimate": 0},
        }

    filtered = []
    for u in units:
        if u.get("authority") in authorities:
            filtered.append(u)
        elif u.get("risk") in risks:
            filtered.append(u)
        elif u.get("type") in types:
            filtered.append(u)
        elif min_attention > 0 and u.get("attention", 0) >= min_attention:
            filtered.append(u)

    # Build text with optional heading context
    parts = []
    for u in filtered:
        text_part = u["text"]
        if include_headings and u.get("heading"):
            heading_prefix = " > ".join(u.get("heading_path", [u["heading"]]))
            text_part = f"[{heading_prefix}]\n{text_part}"
        parts.append(text_part)

    joined = "\n\n".join(parts)

    # Token truncation (~4 chars/token for English)
    if max_tokens > 0:
        max_chars = max_tokens * 4
        if len(joined) > max_chars:
            joined = joined[:max_chars]

    token_estimate = len(joined) // 4
    input_count = len(units)
    output_count = len(filtered)
    reduction = round((1 - output_count / max(input_count, 1)) * 100) if input_count > 0 else 0

    return {
        "text": joined,
        "units": filtered,
        "meta": {
            "input_units": input_count,
            "output_units": output_count,
            "reduction_pct": max(0, reduction),
            "token_estimate": token_estimate,
        },
    }
