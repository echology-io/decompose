#!/usr/bin/env python3
"""Benchmark decompose against reference fixtures. Outputs JSON."""

import json
import sys
import time
from pathlib import Path

from decompose.core import decompose_text

FIXTURES = Path(__file__).parent.parent / "tests" / "fixtures"


def bench_file(path: Path) -> dict:
    text = path.read_text()
    start = time.monotonic()
    result = decompose_text(text)
    elapsed = round((time.monotonic() - start) * 1000, 1)

    meta = result["meta"]
    units = result["units"]

    safety = sum(1 for u in units if u["risk"] == "safety_critical")
    mandatory = sum(1 for u in units if u["authority"] == "mandatory")
    irreducible = sum(1 for u in units if u["irreducible"])

    return {
        "file": path.name,
        "input_chars": len(text),
        "input_words": len(text.split()),
        "total_units": meta["total_units"],
        "processing_ms": elapsed,
        "standards_found": len(meta["standards_found"]),
        "dates_found": len(meta["dates_found"]),
        "token_estimate": meta["token_estimate"],
        "mandatory_units": mandatory,
        "safety_critical_units": safety,
        "irreducible_units": irreducible,
    }


def main():
    if not FIXTURES.exists():
        print(f"No fixtures at {FIXTURES}", file=sys.stderr)
        sys.exit(1)

    files = sorted(FIXTURES.glob("*.txt"))
    if not files:
        print("No .txt fixtures found", file=sys.stderr)
        sys.exit(1)

    results = []
    for f in files:
        results.append(bench_file(f))

    # Summary
    total_chars = sum(r["input_chars"] for r in results)
    total_ms = sum(r["processing_ms"] for r in results)
    total_units = sum(r["total_units"] for r in results)
    total_standards = sum(r["standards_found"] for r in results)

    output = {
        "benchmarks": results,
        "summary": {
            "files": len(results),
            "total_chars": total_chars,
            "total_units": total_units,
            "total_standards": total_standards,
            "total_ms": round(total_ms, 1),
            "chars_per_ms": round(total_chars / max(total_ms, 0.1)),
        },
    }

    json.dump(output, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
