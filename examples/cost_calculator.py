"""Token cost calculator: measure what Decompose saves you.

Decomposes a document and prints before/after token estimates.
Shows exactly how many units need LLM analysis vs. how many get skipped.

Usage:
    python examples/cost_calculator.py
    python examples/cost_calculator.py path/to/your/document.md
"""

import sys
from decompose import decompose_text

SAMPLE_TEXT = """\
The contractor shall provide all materials per ASTM C150-20. Maximum load
shall not exceed 500 psf per ASCE 7-22. Notice to proceed within 14 calendar
days of contract execution. Retainage of 10% applies to all payments.
For general background, the project is located in Denver, CO and follows
standard municipal permitting procedures. The owner reserves the right to
inspect all work at any time during normal business hours. Standard working
hours are defined as 7:00 AM to 5:00 PM, Monday through Friday. The project
manager shall submit weekly progress reports to the owner's representative.
"""

# Rough token estimate: ~4 chars per token for English text
CHARS_PER_TOKEN = 4

# Claude Sonnet input pricing: $3 per 1M tokens
COST_PER_MILLION_TOKENS = 3.00


def estimate_tokens(text: str) -> int:
    return len(text) // CHARS_PER_TOKEN


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
    else:
        text = SAMPLE_TEXT

    result = decompose_text(text)
    units = result["units"]

    total_chars = sum(len(u["text"]) for u in units)
    total_tokens = estimate_tokens(text)

    # With Decompose: only send high-attention units to the LLM
    high_attention = [u for u in units if u["attention"] >= 1.0]
    filtered_chars = sum(len(u["text"]) for u in high_attention)
    filtered_tokens = filtered_chars // CHARS_PER_TOKEN

    reduction_pct = 100 - (filtered_tokens * 100 // total_tokens) if total_tokens > 0 else 0

    print(f"--- Before Decompose (send everything to LLM) ---")
    print(f"  Units:      {len(units)}")
    print(f"  Characters: {total_chars:,}")
    print(f"  Est tokens: {total_tokens:,}")

    print(f"\n--- After Decompose (send attention >= 1.0 only) ---")
    print(f"  Units:      {len(high_attention)}")
    print(f"  Characters: {filtered_chars:,}")
    print(f"  Est tokens: {filtered_tokens:,}")

    print(f"\n--- Savings ---")
    print(f"  Token reduction:  {reduction_pct}%")
    print(f"  At 10K docs/month:")
    before_cost = total_tokens * 10_000 * COST_PER_MILLION_TOKENS / 1_000_000
    after_cost = filtered_tokens * 10_000 * COST_PER_MILLION_TOKENS / 1_000_000
    print(f"    Before: ${before_cost:,.2f}/month")
    print(f"    After:  ${after_cost:,.2f}/month")
    print(f"    Saved:  ${before_cost - after_cost:,.2f}/month")


if __name__ == "__main__":
    main()
