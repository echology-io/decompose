"""Authority, risk, and content type classification — pure regex, no LLM."""

from __future__ import annotations

import re
from dataclasses import dataclass

# ── Authority patterns ────────────────────────────────────────────
# Universal language-level patterns. "shall" means mandatory in every
# industry, every document type. These are language constructs, not
# domain heuristics.

AUTHORITY_PATTERNS: dict[str, dict] = {
    "mandatory": {
        "patterns": [
            r"\bshall\b(?!\s+not)", r"\bmust\b(?!\s+not)", r"\bis\s+required\b",
            r"\bare\s+required\b", r"\bshall\s+comply\b", r"\bshall\s+conform\b",
            r"\bmandatory\b", r"\brequired\s+to\b", r"\bwill\s+be\s+required\b",
        ],
        "weight": 1.0,
    },
    "prohibitive": {
        "patterns": [
            r"\bshall\s+not\b", r"\bmust\s+not\b", r"\bprohibit(?:ed|s)?\b",
            r"\bforbid(?:den|s)?\b", r"\bnot\s+permitted\b",
            r"\bunder\s+no\s+circumstances\b",
        ],
        "weight": 1.0,
    },
    "directive": {
        "patterns": [
            r"\bshould\b(?!\s+not)", r"\brecommend(?:ed|s)?\b",
            r"\bexpect(?:ed|s)?\b", r"\bis\s+to\b", r"\bare\s+to\b",
            r"\badvised\s+to\b",
        ],
        "weight": 0.75,
    },
    "permissive": {
        "patterns": [
            r"\bmay\b", r"\bcan\b", r"\bpermit(?:ted|s)?\b", r"\bacceptable\b",
            r"\ballow(?:ed|s|able)?\b", r"\bat\s+the\s+(?:discretion|option)\b",
            r"\boption(?:al|ally)?\b",
        ],
        "weight": 0.35,
    },
    "informational": {
        "patterns": [
            r"\bfor\s+information\b", r"\bnote\s*(?::|that)\b",
            r"\binformational\s+only\b", r"\bfor\s+reference\b", r"\bfyi\b",
            r"\bnon-?binding\b",
        ],
        "weight": 0.25,
    },
    "conditional": {
        "patterns": [
            r"\bif\b[^.!?\n]*\bthen\b", r"\bwhen\b[^.!?\n]*\bshall\b", r"\bunless\b",
            r"\bexcept\s+(?:where|when|as)\b", r"\bprovided\s+that\b",
            r"\bsubject\s+to\b", r"\bin\s+the\s+event\b",
        ],
        "weight": 0.60,
    },
}

# ── Risk patterns ─────────────────────────────────────────────────

RISK_PATTERNS: dict[str, list[str]] = {
    "safety_critical": [
        r"\blife\s+safety\b", r"\bseismic\b", r"\bcollapse\b",
        r"\bfire\s+(?:rated?|resistance|protection|safety)\b",
        r"\bstructural\s+(?:integrity|failure|capacity)\b",
        r"\bemergency\b", r"\bhazard(?:ous)?\b",
    ],
    "security": [
        r"\battack(?:er|s)?\b", r"\bunauthorized\s+access\b",
        r"\bvulnerabilit(?:y|ies)\b", r"\bmalicious\b", r"\bmalware\b",
        r"\bexploit(?:ation)?\b", r"\bauthenticat(?:ion|e|ed)\b",
        r"\brebinding\b", r"\binjection\b", r"\bbreach(?:es)?\b",
    ],
    "compliance": [
        r"\bshall\s+comply\b", r"\bin\s+accordance\s+with\b",
        r"\bcode\s+(?:compliance|requirement)\b", r"\bregulat(?:ion|ory)\b",
        r"\binspection\b", r"\bpermit(?:ting)?\b",
    ],
    "financial": [
        r"\$\s*[\d,]+", r"\bretainage\b", r"\bliquidated\s+damages\b",
        r"\bpayment\b", r"\bcontract\s+(?:value|amount|sum)\b",
        r"\bchange\s+order\b",
    ],
    "contractual": [
        r"\bindemnif(?:y|ication)\b", r"\bliabilit(?:y|ies)\b",
        r"\bwarrant(?:y|ies)\b", r"\btermination\b",
        r"\bforce\s+majeure\b",
    ],
    "advisory": [
        r"\bfor\s+(?:your\s+)?information\b", r"\bfyi\b",
        r"\bgeneral\s+(?:information|guidance)\b",
    ],
}

# ── Content type patterns ─────────────────────────────────────────

CONTENT_TYPE_PATTERNS: dict[str, list[str]] = {
    "requirement": [r"\bshall\b", r"\bmust\b", r"\brequired\b"],
    "definition": [
        r"\bmeans\b", r"\bis\s+defined\s+as\b", r"\brefers?\s+to\b",
        r"\bhereinafter\b", r"\bfor\s+purposes?\s+of\b",
    ],
    "reference": [
        r"\bin\s+accordance\s+with\b", r"\bper\s+(?:section|article)\b",
        r"\bsee\s+(?:section|appendix)\b", r"\brefer\s+to\b",
        r"\bas\s+(?:specified|described|defined)\s+in\b",
    ],
    "constraint": [r"\bnot\s+(?:to\s+)?exceed\b", r"\bmaximum\b", r"\bminimum\b", r"\btolerance\b"],
    "narrative": [r"\bbackground\b", r"\boverview\b", r"\bintroduction\b", r"\bsummary\b"],
    "data": [r"\btable\b", r"\bfigure\b", r"\bschedule\b", r"\bappendix\b"],
}


@dataclass(slots=True)
class Classification:
    authority: str = "informational"
    authority_score: float = 0.0
    risk: str = "informational"
    risk_score: float = 0.0
    content_type: str = "narrative"
    actionable: bool = False
    attention: float = 0.0


def _score_patterns(text: str, patterns: dict[str, dict | list[str]], use_weight: bool = False) -> tuple[str, float]:
    """Score text against a pattern dict. Returns (top_label, score)."""
    scores: dict[str, float] = {}
    text_lower = text.lower() if len(text) < 50_000 else text[:50_000].lower()

    for label, value in patterns.items():
        pats = value["patterns"] if isinstance(value, dict) else value
        weight = value.get("weight", 1.0) if isinstance(value, dict) else 1.0
        count = 0
        for p in pats:
            count += len(re.findall(p, text_lower, re.IGNORECASE))
        if count > 0:
            scores[label] = count * weight

    if not scores:
        return ("informational", 0.0)

    top = max(scores, key=scores.get)  # type: ignore[arg-type]
    return (top, scores[top])


def classify(text: str) -> Classification:
    """Classify a text passage. Pure regex, no LLM, deterministic."""
    authority, auth_score = _score_patterns(text, AUTHORITY_PATTERNS, use_weight=True)
    risk, risk_score = _score_patterns(text, RISK_PATTERNS)
    content_type, _ = _score_patterns(text, CONTENT_TYPE_PATTERNS)

    # Attention score: risk multiplier * normalized authority score
    risk_mult = {
        "safety_critical": 4.0, "security": 3.0, "compliance": 2.0,
        "financial": 1.5, "contractual": 1.5, "advisory": 0.5,
        "informational": 0.3,
    }.get(risk, 0.5)
    attention = min(10.0, round(min(auth_score, 5.0) * risk_mult, 1))

    actionable = (
        authority in ("mandatory", "prohibitive", "directive")
        or risk in ("safety_critical", "security", "compliance")
    )

    return Classification(
        authority=authority,
        authority_score=round(min(auth_score, 10.0), 2),
        risk=risk,
        risk_score=round(min(risk_score, 10.0), 2),
        content_type=content_type,
        actionable=actionable,
        attention=attention,
    )
