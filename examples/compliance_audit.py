"""Compliance audit trail: deterministic, reproducible classification.

Decomposes a document and prints a full audit trail for each unit.
Every classification is traceable to the patterns that triggered it.
Run it twice on the same input -- you get the same output every time.

Usage:
    python examples/compliance_audit.py
    python examples/compliance_audit.py path/to/your/document.md
"""

import json
import sys
from decompose import decompose_text

SAMPLE_TEXT = """\
The contractor shall provide all materials per ASTM C150-20. Maximum load
shall not exceed 500 psf per ASCE 7-22. All workers must wear hard hats
and safety vests on site at all times per OSHA 1926.100. Retainage of 10%
applies to all payments. Liquidated damages of $500/day for delays beyond
the substantial completion date. The project is located in Denver, CO.
"""


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
    else:
        text = SAMPLE_TEXT

    result = decompose_text(text)
    units = result["units"]

    print(f"=== Compliance Audit Trail ===")
    print(f"Input: {len(text)} characters")
    print(f"Units: {len(units)}")
    print()

    for i, unit in enumerate(units, 1):
        print(f"--- Unit {i} ---")
        print(f"  Text:         {unit['text'][:80]}")
        print(f"  Authority:    {unit['authority']}")
        print(f"  Risk:         {unit['risk']}")
        print(f"  Attention:    {unit['attention']}")
        print(f"  Irreducible:  {unit.get('irreducible', False)}")
        print(f"  Actionable:   {unit.get('actionable', False)}")

        entities = unit.get("entities", [])
        if entities:
            print(f"  Entities:     {', '.join(entities)}")

        financial = unit.get("financial", [])
        if financial:
            print(f"  Financial:    {', '.join(str(f) for f in financial)}")

        dates = unit.get("dates", [])
        if dates:
            print(f"  Dates:        {', '.join(dates)}")

        print()

    # Summary stats
    mandatory = [u for u in units if u["authority"] in ("mandatory", "prohibitive")]
    irreducible = [u for u in units if u.get("irreducible")]
    safety = [u for u in units if u["risk"] == "safety_critical"]

    print(f"=== Summary ===")
    print(f"  Mandatory/prohibitive: {len(mandatory)} units")
    print(f"  Irreducible:           {len(irreducible)} units")
    print(f"  Safety-critical:       {len(safety)} units")
    print(f"\nDeterministic: run this again on the same input and every value is identical.")


if __name__ == "__main__":
    main()
