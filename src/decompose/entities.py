"""Entity extraction — standards, dates, parties, financial terms."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ── Standards and code references ─────────────────────────────────

_STANDARD_US = re.compile(
    r"\b(ASTM|ASCE|ACI|AISC|ASHRAE|AWS|AASHTO|NFPA|IEEE|ANSI|UL|FM|ASME)"
    r"\s*[/-]?\s*([A-Z]?\d{1,5}(?:[./]\d+)?)\s*(?:[-/]\s*(\d{2,4}))?\b"
)
_STANDARD_INTL = re.compile(
    r"\b(ISO|EN|BS|DIN|JIS|AS|NZS|CSA|CEN|IEC)"
    r"\s*(\d{3,6}(?:[.-]\d+)?)\s*(?:[-:]\s*(\d{4}))?\b"
)
_BUILDING_CODE = re.compile(
    r"\b(IBC|IRC|IPC|IMC|IFC|IECC|NEC|NBC|NBCC|Eurocode\s*\d?)"
    r"\s*(\d{4})?\b"
)
_OSHA = re.compile(r"\bOSHA\s*(?:29\s*CFR\s*)?(\d{4}\.\d+)\b")
_CFR = re.compile(r"\b(\d+)\s+C\.?F\.?R\.?\s*(?:(?:Part|§)\s*)?(\d+(?:\.\d+)?)\b")

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

    # Standards
    for rx in (_STANDARD_US, _STANDARD_INTL, _BUILDING_CODE, _OSHA):
        for m in rx.finditer(text):
            standards.append(m.group(0).strip())

    # CFR references
    for m in _CFR.finditer(text):
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
