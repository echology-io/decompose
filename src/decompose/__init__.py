"""Decompose — Structured intelligence from any text.

Deterministic text classification for AI agents. No LLM required.
"""

__version__ = "0.2.0"

from decompose.core import decompose, decompose_text, filter_for_llm

__all__ = ["decompose", "decompose_text", "filter_for_llm", "__version__"]
