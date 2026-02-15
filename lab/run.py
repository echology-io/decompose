#!/usr/bin/env python3
"""Testing lab — run decompose against real documents and generate a report."""

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from decompose.core import decompose_text


def process_file(path: Path) -> dict:
    """Process a single file and return detailed results."""
    text = path.read_text(errors="replace")
    if not text.strip():
        return {"file": path.name, "error": "empty"}

    # Timing (100 iterations for stable measurement)
    start = time.monotonic()
    iterations = 100
    for _ in range(iterations):
        result = decompose_text(text)
    avg_ms = round((time.monotonic() - start) * 1000 / iterations, 2)

    units = result["units"]
    meta = result["meta"]

    # Unit breakdown
    authority_dist = {}
    risk_dist = {}
    type_dist = {}
    high_attention = []
    irreducible_units = []

    for i, u in enumerate(units):
        auth = u["authority"]
        authority_dist[auth] = authority_dist.get(auth, 0) + 1

        risk = u.get("risk", "informational")
        risk_dist[risk] = risk_dist.get(risk, 0) + 1

        ctype = u.get("type", "narrative")
        type_dist[ctype] = type_dist.get(ctype, 0) + 1

        if u["attention"] >= 3.0:
            high_attention.append({
                "unit": i + 1,
                "heading": u.get("heading", "(none)"),
                "attention": u["attention"],
                "authority": auth,
                "risk": risk,
                "preview": u["text"][:120].replace("\n", " "),
            })

        if u["irreducible"]:
            irreducible_units.append({
                "unit": i + 1,
                "heading": u.get("heading", "(none)"),
                "recommendation": u.get("irreducibility", "PRESERVE_VERBATIM"),
                "preview": u["text"][:120].replace("\n", " "),
            })

    return {
        "file": path.name,
        "chars": len(text),
        "words": len(text.split()),
        "avg_ms": avg_ms,
        "total_units": len(units),
        "authority_distribution": authority_dist,
        "risk_distribution": risk_dist,
        "type_distribution": type_dist,
        "standards_found": meta.get("standards_found", []),
        "dates_found": meta.get("dates_found", []),
        "high_attention_units": high_attention,
        "irreducible_units": irreducible_units,
        "summary": {
            "actionable": sum(1 for u in units if u.get("actionable")),
            "irreducible": len(irreducible_units),
            "high_attention": len(high_attention),
            "max_attention": max((u["attention"] for u in units), default=0),
        },
    }


def print_report(results: list[dict]):
    """Print a human-readable report to stdout."""
    print("=" * 70)
    print("DECOMPOSE TESTING LAB — REPORT")
    print("=" * 70)

    total_chars = 0
    total_words = 0
    total_units = 0
    total_ms = 0.0

    for r in results:
        if "error" in r:
            print(f"\n  {r['file']}: SKIPPED ({r['error']})")
            continue

        total_chars += r["chars"]
        total_words += r["words"]
        total_units += r["total_units"]
        total_ms += r["avg_ms"]

        print(f"\n{'─' * 70}")
        print(f"  {r['file']}")
        print(f"  {r['chars']:,} chars | {r['words']:,} words | {r['avg_ms']}ms")
        print(f"  {r['total_units']} units | "
              f"{r['summary']['actionable']} actionable | "
              f"{r['summary']['irreducible']} irreducible | "
              f"max attention: {r['summary']['max_attention']}")

        print(f"\n  Authority: {r['authority_distribution']}")
        print(f"  Risk:      {r['risk_distribution']}")
        print(f"  Type:      {r['type_distribution']}")

        if r["standards_found"]:
            print(f"  Standards: {r['standards_found']}")

        if r["high_attention_units"]:
            print(f"\n  High-attention units:")
            for u in r["high_attention_units"]:
                print(f"    [{u['attention']}] {u['heading']} "
                      f"({u['authority']}/{u['risk']})")
                print(f"         {u['preview']}...")

        if r["irreducible_units"]:
            print(f"\n  Irreducible units:")
            for u in r["irreducible_units"]:
                print(f"    [{u['recommendation']}] {u['heading']}")
                print(f"         {u['preview']}...")

    print(f"\n{'=' * 70}")
    print(f"  TOTALS")
    print(f"  {len(results)} docs | {total_chars:,} chars | "
          f"{total_words:,} words | {total_units} units")
    print(f"  {round(total_ms, 1)}ms total | "
          f"{round(total_ms / max(len(results), 1), 1)}ms avg/doc | "
          f"{round(total_chars / max(total_ms, 0.1))} chars/ms")
    print(f"{'=' * 70}")


def main():
    # Find test documents
    test_dir = Path(__file__).resolve().parent.parent / "docs" / "tests"

    if not test_dir.exists():
        print(f"No test directory at {test_dir}", file=sys.stderr)
        sys.exit(1)

    # Collect all text files recursively
    files = sorted(
        p for p in test_dir.rglob("*")
        if p.suffix in (".md", ".txt", ".rst") and p.is_file()
    )

    if not files:
        print(f"No documents found in {test_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(files)} documents in {test_dir}\n")

    results = []
    for f in files:
        results.append(process_file(f))

    # Print human-readable report
    print_report(results)

    # Save detailed results
    root = Path(__file__).resolve().parent.parent
    out_path = root / "lab" / "results.json"
    with open(out_path, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\nFull results saved to {out_path}")

    # Build site-facing benchmarks
    valid = [r for r in results if "error" not in r]
    total_chars = sum(r["chars"] for r in valid)
    total_words = sum(r["words"] for r in valid)
    total_units = sum(r["total_units"] for r in valid)
    total_ms = sum(r["avg_ms"] for r in valid)
    total_irreducible = sum(r["summary"]["irreducible"] for r in valid)
    total_actionable = sum(r["summary"]["actionable"] for r in valid)
    avg_ms = round(total_ms / max(len(valid), 1), 1)
    chars_per_ms = round(total_chars / max(total_ms, 0.1))

    irr_pct = round(total_irreducible / max(total_units, 1) * 100)

    # Count passing tests
    test_count = 0
    try:
        out = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "--co", "-q"],
            capture_output=True, text=True, cwd=str(root),
        )
        for line in out.stdout.splitlines():
            if "collected" in line:
                parts = line.strip().split()
                if parts and parts[0].isdigit():
                    test_count = int(parts[0])
    except Exception:
        pass

    benchmarks = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "docs": len(valid),
        "total_chars": total_chars,
        "total_words": total_words,
        "total_units": total_units,
        "avg_ms": avg_ms,
        "chars_per_ms": chars_per_ms,
        "irreducible": total_irreducible,
        "irreducible_pct": irr_pct,
        "actionable": total_actionable,
        "tests": test_count,
        "files": [
            {
                "file": r["file"],
                "chars": r["chars"],
                "words": r["words"],
                "units": r["total_units"],
                "ms": r["avg_ms"],
                "irreducible": r["summary"]["irreducible"],
                "actionable": r["summary"]["actionable"],
            }
            for r in valid
        ],
    }

    bench_path = root / "docs" / "benchmarks.json"
    with open(bench_path, "w") as fp:
        json.dump(benchmarks, fp, indent=2)
    print(f"Site benchmarks saved to {bench_path}")


if __name__ == "__main__":
    main()
