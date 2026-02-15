"""Core decompose pipeline — the single function that does everything."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field

from decompose.chunker import Chunk, auto_chunk
from decompose.classifier import Classification, classify
from decompose.entities import Entities, extract_entities
from decompose.irreducibility import IrreducibilityResult, detect_irreducibility


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
            "_decompose": "0.1.0",
        },
    }


# Convenience alias
decompose = decompose_text
