"""Attention-filtered RAG: only embed what matters.

Decomposes a document, filters by attention score, and shows which units
would enter your vector store vs. which get skipped. No external deps
beyond decompose-mcp.

Usage:
    python examples/rag_pipeline.py
    python examples/rag_pipeline.py path/to/your/document.md
"""

import sys
from decompose import decompose_text

SAMPLE_TEXT = """\
The contractor shall provide all materials per ASTM C150-20. Maximum load
shall not exceed 500 psf per ASCE 7-22. Notice to proceed within 14 calendar
days of contract execution. Retainage of 10% applies to all payments.
For general background, the project is located in Denver, CO and follows
standard municipal permitting procedures. The owner reserves the right to
inspect all work at any time during normal business hours.
"""

ATTENTION_THRESHOLD = 2.0


def mock_embed(text: str) -> list[float]:
    """Stand-in for your real embedding function."""
    return [0.0] * 8  # Replace with your embedding model


def main():
    # Load text from file or use the sample
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
    else:
        text = SAMPLE_TEXT

    result = decompose_text(text)
    units = result["units"]

    embedded = []
    skipped = []

    for unit in units:
        if unit["attention"] >= ATTENTION_THRESHOLD:
            embedding = mock_embed(unit["text"])
            embedded.append(unit)
            print(f"  EMBED  [{unit['attention']:4.1f}] [{unit['authority']:12s}] {unit['text'][:70]}")
        else:
            skipped.append(unit)
            print(f"  SKIP   [{unit['attention']:4.1f}] [{unit['authority']:12s}] {unit['text'][:70]}")

    print(f"\n--- Results ---")
    print(f"Total units:    {len(units)}")
    print(f"Embedded:       {len(embedded)} (attention >= {ATTENTION_THRESHOLD})")
    print(f"Skipped:        {len(skipped)}")
    print(f"Token reduction: ~{len(skipped) * 100 // len(units)}%")


if __name__ == "__main__":
    main()
