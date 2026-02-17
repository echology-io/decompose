"""Risk-based routing: send each unit to the right handler.

Decomposes a document and routes units by risk category. Safety-critical
content goes to one chain, financial to another, boilerplate gets skipped.

Usage:
    python examples/agent_router.py
    python examples/agent_router.py path/to/your/document.md
"""

import sys
from decompose import decompose_text

SAMPLE_TEXT = """\
The contractor shall provide all materials per ASTM C150-20. Maximum load
shall not exceed 500 psf per ASCE 7-22. All workers must wear hard hats
and safety vests on site at all times per OSHA 1926.100. Notice to proceed
within 14 calendar days of contract execution. Retainage of 10% applies
to all payments. Liquidated damages of $500/day for delays beyond the
substantial completion date. For general background, the project is located
in Denver, CO and follows standard municipal permitting procedures.
"""


def safety_chain(unit: dict):
    """Full analysis + human review flag."""
    print(f"  [SAFETY]    {unit['text'][:70]}")
    print(f"              entities: {unit.get('entities', [])}")


def financial_chain(unit: dict):
    """Flag for finance team review."""
    print(f"  [FINANCIAL] {unit['text'][:70]}")
    print(f"              financial: {unit.get('financial', [])}")


def compliance_chain(unit: dict):
    """Standard compliance check."""
    print(f"  [COMPLIANCE]{unit['text'][:70]}")


def general_chain(unit: dict):
    """Standard LLM analysis."""
    print(f"  [GENERAL]   {unit['text'][:70]}")


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
    else:
        text = SAMPLE_TEXT

    result = decompose_text(text)
    units = result["units"]

    routed = {"safety": 0, "financial": 0, "compliance": 0, "general": 0, "skipped": 0}

    for unit in units:
        if unit["risk"] == "safety_critical":
            safety_chain(unit)
            routed["safety"] += 1
        elif unit["risk"] == "financial":
            financial_chain(unit)
            routed["financial"] += 1
        elif unit["risk"] == "compliance":
            compliance_chain(unit)
            routed["compliance"] += 1
        elif unit["attention"] < 0.5:
            print(f"  [SKIP]      {unit['text'][:70]}")
            routed["skipped"] += 1
        else:
            general_chain(unit)
            routed["general"] += 1

    print(f"\n--- Routing Summary ---")
    for chain, count in routed.items():
        if count > 0:
            print(f"  {chain:12s}: {count} units")
    print(f"  {'total':12s}: {len(units)} units")


if __name__ == "__main__":
    main()
