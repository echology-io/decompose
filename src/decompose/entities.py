"""Entity extraction — standards, dates, parties, financial terms."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ── Standards and code references ─────────────────────────────────
# Universal standards bodies only. Domain-specific standards (AEC, medical,
# etc.) are handled by the engine's domain system, not here.

_STANDARD_INTL = re.compile(
    r"\b(ISO|EN|BS|DIN|JIS|AS|NZS|CSA|CEN|IEC|IEEE|ANSI|UL|ASME)"
    r"\s*[/-]?\s*([A-Z]?\d{1,6}(?:[.-]\d+)?)\s*(?:[-/:]\s*(\d{2,4}))?\b"
)

# Legal/regulatory references
_CFR = re.compile(r"\b(\d+)\s+C\.?F\.?R\.?\s*(?:(?:Part|§)\s*)?(\d+(?:\.\d+)?)\b")
_USC = re.compile(r"\b(\d+)\s+U\.?S\.?C\.?\s*§?\s*(\d+)\b")

# ── Dates ─────────────────────────────────────────────────────────

_DATE_MDY = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b")
_DATE_WRITTEN = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(\d{1,2}),?\s+(\d{4})\b",
    re.IGNORECASE,
)

# ── Financial ─────────────────────────────────────────────────────

_DOLLAR = re.compile(r"\$\s*([\d,]+(?:\.\d{2})?)\b")
_PERCENT = re.compile(r"(\d+(?:\.\d+)?)%")


@dataclass(slots=True)
class Entities:
    standards: list[str] = field(default_factory=list)
    dates: list[str] = field(default_factory=list)
    financial: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)


def extract_entities(text: str) -> Entities:
    """Extract structured entities from text. Pure regex, deterministic."""
    standards: list[str] = []
    dates: list[str] = []
    financial: list[str] = []
    references: list[str] = []

    # Standards (universal bodies only)
    for m in _STANDARD_INTL.finditer(text):
        standards.append(m.group(0).strip())

    # Legal/regulatory references
    for rx in (_CFR, _USC):
        for m in rx.finditer(text):
            references.append(m.group(0).strip())

    # Dates
    for m in _DATE_MDY.finditer(text):
        dates.append(m.group(0))
    for m in _DATE_WRITTEN.finditer(text):
        dates.append(m.group(0))

    # Financial
    for m in _DOLLAR.finditer(text):
        financial.append(f"${m.group(1)}")
    for m in _PERCENT.finditer(text):
        financial.append(f"{m.group(1)}%")

    # Deduplicate preserving order
    return Entities(
        standards=list(dict.fromkeys(standards)),
        dates=list(dict.fromkeys(dates)),
        financial=list(dict.fromkeys(financial)),
        references=list(dict.fromkeys(references)),
    )
