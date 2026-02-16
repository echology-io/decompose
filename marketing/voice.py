"""Voice corpus loader — style guide and few-shot samples."""

import json
from pathlib import Path

from marketing.config import VOICE_DIR


def load_style_guide() -> str:
    """Load the codified voice rules as a string for prompt injection."""
    path = VOICE_DIR / "style_guide.md"
    if path.exists():
        return path.read_text()
    return ""


def load_samples() -> list[dict]:
    """Load representative writing samples with annotations."""
    path = VOICE_DIR / "samples.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


def format_samples_for_prompt(samples: list[dict]) -> str:
    """Format samples into a prompt-ready string for few-shot context."""
    if not samples:
        return ""
    parts = ["REFERENCE EXAMPLES — match this voice:\n"]
    for s in samples:
        parts.append(f'[{s["type"]}]\n"{s["text"]}"\n')
    return "\n".join(parts)
