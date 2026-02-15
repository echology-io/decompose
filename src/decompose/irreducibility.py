"""Irreducibility detection — identify content that must be preserved verbatim."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

IRREDUCIBLE_PATTERNS: list[tuple[str, str]] = [
    (r"\bshall\s+(?:not\s+)?(?:be|provide|install|submit|comply)\b", "legal_mandate"),
    (r"\b\d+(?:\.\d+)?\s*(?:psf|psi|ksi|kip|lb|kN|MPa|mm|in\.?|ft)\b", "engineering_value"),
    (r"\bNOT\s+(?:TO\s+)?(?:EXCEED|LESS\s+THAN)\b", "limit_specification"),
    (r"\b(?:minimum|maximum|exact|precisely|tolerance)\b[^.!?\n]*\b\d", "precision_requirement"),
    (r"\b(?:ARTICLE|SECTION|CLAUSE)\s+\d+(?:\.\d+)*\b", "legal_reference"),
    (r"\bformula\b[^.!?\n]*[=+\-*/]", "mathematical_formula"),
    (r"\b(?:specification|spec)\s+(?:no\.?|#|number)\s*\d", "specification_id"),
    (r"\b(?:warranty|guarantee|indemnif|liability)\b", "legal_obligation"),
    (r"\$\s*[\d,]+(?:\.\d{2})?\b", "financial_value"),
    (r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "date_reference"),
]


@dataclass(slots=True)
class IrreducibilityResult:
    irreducible: bool
    confidence: float
    recommendation: str
    categories: list[str] = field(default_factory=list)
    match_count: int = 0


def detect_irreducibility(text: str) -> IrreducibilityResult:
    """Determine if text content is computationally irreducible."""
    matches = []
    categories_seen: set[str] = set()

    for pattern, category in IRREDUCIBLE_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            matches.append(m.group(0)[:80])
            categories_seen.add(category)

    count = len(matches)
    confidence = min(1.0, count * 0.2)

    if confidence >= 0.6:
        rec = "PRESERVE_VERBATIM"
    elif confidence >= 0.3:
        rec = "PRESERVE_KEY_VALUES"
    else:
        rec = "SUMMARIZABLE"

    return IrreducibilityResult(
        irreducible=count > 0,
        confidence=round(confidence, 3),
        recommendation=rec,
        categories=sorted(categories_seen),
        match_count=count,
    )
