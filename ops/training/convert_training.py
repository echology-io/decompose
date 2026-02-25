#!/usr/bin/env python3
"""
convert_training.py — Convert Vanta training JSONL to Ollama chat-format pairs.

Reads rich semantic unit records from data/training/*.jsonl, converts each into
Ollama-ready instruction/response chat pairs (3 task types), and writes output
to data/aecai_training/.

Usage:
    python3 convert_training.py
    python3 convert_training.py --input-dir data/training/ --output-dir data/aecai_training/
    python3 convert_training.py --deduplicate
"""

import argparse
import json
import sys
from pathlib import Path

SYSTEM_CLASSIFY = (
    "You are AECai, an expert AEC document analyst. Classify the document and extract structured metadata."
)
SYSTEM_RISK = (
    "You are AECai, an expert AEC document analyst. "
    "Assess the authority level and risk implications of document content."
)
SYSTEM_SUMMARY = (
    "You are AECai, an expert AEC document analyst. Summarize document content and identify key relationships."
)

MODELFILE_TEMPLATE = """\
FROM llama3
ADAPTER ./aecai-lora.gguf
SYSTEM "You are AECai, an expert analyst for Architecture, Engineering, and Construction (AEC) documents. You classify documents, extract structured metadata, assess authority levels and risk, and identify standards references, entities, and obligations."
PARAMETER temperature 0.3
PARAMETER top_p 0.9
"""


def _safe(val, default=""):
    """Return val if truthy, else default."""
    if val is None:
        return default
    if isinstance(val, list):
        return ", ".join(str(v) for v in val) if val else default
    return str(val) if val else default


def _format_entities(entities):
    """Format entity list into readable string."""
    if not entities:
        return "None"
    parts = []
    for ent in entities:
        if isinstance(ent, dict):
            parts.append(f"{ent.get('value', '?')} ({ent.get('type', 'unknown')})")
        else:
            parts.append(str(ent))
    return ", ".join(parts) if parts else "None"


def convert_record(record):
    """Convert a single training record into Ollama chat-format pairs.

    Returns a list of dicts, each with a "messages" key containing the chat pair.
    """
    text = record.get("text", "").strip()
    if not text:
        return []

    labels = record.get("labels", {})
    extracted = record.get("extracted", {})
    document = record.get("document", {})
    context = record.get("context", {})
    auth_scores = extracted.get("authority_scores", {})

    pairs = []

    # ── Task A: Classification + Metadata Extraction ──
    assistant_a = (
        f"Document Type: {_safe(document.get('document_type'), 'unknown')}\n"
        f"Content Type: {_safe(labels.get('content_type'), 'other')}\n"
        f"Authority Level: {_safe(labels.get('authority_level'), 'informational')}\n"
        f"Risk Relevance: {_safe(labels.get('risk_relevance'), 'informational')}\n"
        f"Actionable: {labels.get('actionable', False)}\n"
        f"Domains: {_safe(labels.get('domain_tags'))}\n"
        f"Standards Referenced: {_safe(record.get('linked_standards'))}\n"
        f"Entities: {_format_entities(extracted.get('entities'))}"
    )

    pairs.append(
        {
            "messages": [
                {"role": "system", "content": SYSTEM_CLASSIFY},
                {"role": "user", "content": f"Analyze this AEC document excerpt:\n\n{text}"},
                {"role": "assistant", "content": assistant_a},
            ]
        }
    )

    # ── Task B: Risk & Authority Assessment ──
    m = auth_scores.get("mandatory", 0)
    d = auth_scores.get("directive", 0)
    c = auth_scores.get("conditional", 0)
    inf = auth_scores.get("informational", 0)
    p = auth_scores.get("prohibitive", 0)
    conf = auth_scores.get("confidence", 0)

    assistant_b = (
        f"Authority Scores: mandatory={m}, directive={d}, conditional={c}, "
        f"informational={inf}, prohibitive={p} (confidence: {conf})\n"
        f"Risk: {_safe(labels.get('risk_relevance'), 'informational')}\n"
        f"Requires Human Review: {record.get('requires_human_review', False)}\n"
        f"Risk Summary: {_safe(document.get('risk_summary'), 'No specific risk summary available.')}"
    )

    pairs.append(
        {
            "messages": [
                {"role": "system", "content": SYSTEM_RISK},
                {"role": "user", "content": f"Evaluate the authority and risk of this AEC content:\n\n{text}"},
                {"role": "assistant", "content": assistant_b},
            ]
        }
    )

    # ── Task C: Summary & Context (only for units with word_count > 50) ──
    word_count = context.get("word_count", 0)
    if word_count > 50:
        project = document.get("project", {})
        parties = document.get("parties", {})

        assistant_c = (
            f"Summary: {_safe(document.get('content_summary'), 'No summary available.')}\n"
            f"Project: {_safe(project.get('number'))} — "
            f"{_safe(project.get('location'))} ({_safe(project.get('date'))})\n"
            f"Parties: {_safe(parties.get('author'))} (author), "
            f"{_safe(parties.get('client'))} (client)\n"
            f"Key Entities: {_safe(record.get('linked_entities'))}\n"
            f"Standards: {_safe(record.get('linked_standards'))}"
        )

        pairs.append(
            {
                "messages": [
                    {"role": "system", "content": SYSTEM_SUMMARY},
                    {
                        "role": "user",
                        "content": (
                            f"Summarize this AEC document section and identify key entities and standards:\n\n{text}"
                        ),
                    },
                    {"role": "assistant", "content": assistant_c},
                ]
            }
        )

    return pairs


def main():
    parser = argparse.ArgumentParser(description="Convert Vanta training JSONL to Ollama chat-format pairs.")
    parser.add_argument(
        "--input-dir",
        default="data/training/",
        help="Directory containing source *.jsonl files (default: data/training/)",
    )
    parser.add_argument(
        "--output-dir",
        default="data/aecai_training/",
        help="Output directory (default: data/aecai_training/)",
    )
    parser.add_argument(
        "--deduplicate",
        action="store_true",
        help="Skip records with duplicate document_id + unit_id",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    jsonl_files = sorted(input_dir.glob("*.jsonl"))
    if not jsonl_files:
        print(f"Error: No .jsonl files found in '{input_dir}'.", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Read and optionally deduplicate records ──
    records = []
    seen_keys = set()
    skipped_dupes = 0
    doc_ids = set()
    files_read = 0

    for jsonl_file in jsonl_files:
        files_read += 1
        for line_num, line in enumerate(jsonl_file.read_text().splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  Warning: {jsonl_file.name}:{line_num} — invalid JSON: {e}", file=sys.stderr)
                continue

            if args.deduplicate:
                doc_id = record.get("document", {}).get("document_id", "")
                unit_id = record.get("unit_id", "")
                key = f"{doc_id}:{unit_id}"
                if key in seen_keys:
                    skipped_dupes += 1
                    continue
                seen_keys.add(key)

            doc_ids.add(record.get("document", {}).get("document_id", "unknown"))
            records.append(record)

    print(f"Read {len(records)} records from {files_read} file(s)")
    if args.deduplicate and skipped_dupes:
        print(f"Deduplicated: skipped {skipped_dupes} duplicate records")

    # ── Convert to Ollama chat pairs ──
    all_pairs = []
    task_counts = {"A": 0, "B": 0, "C": 0}

    for record in records:
        pairs = convert_record(record)
        for i, pair in enumerate(pairs):
            task_label = ["A", "B", "C"][i]
            task_counts[task_label] += 1
        all_pairs.extend(pairs)

    # ── Write output ──
    out_file = output_dir / "aecai_train.jsonl"
    with open(out_file, "w") as f:
        for pair in all_pairs:
            f.write(json.dumps(pair) + "\n")

    # ── Write Modelfile ──
    modelfile_path = output_dir / "Modelfile"
    modelfile_path.write_text(MODELFILE_TEMPLATE)

    # ── Summary ──
    print(f"\nOutput: {out_file}")
    print(f"Modelfile: {modelfile_path}")
    print("\n--- Summary ---")
    print(f"Source files:      {files_read}")
    print(f"Unique documents:  {len(doc_ids)}")
    print(f"Input records:     {len(records)}")
    print(f"Training pairs:    {len(all_pairs)}")
    print(f"  Task A (classify):  {task_counts['A']}")
    print(f"  Task B (risk):      {task_counts['B']}")
    print(f"  Task C (summary):   {task_counts['C']}")


if __name__ == "__main__":
    main()
