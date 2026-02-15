"""Semantic chunking — header-aware Markdown and sentence-boundary text splitting."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

DEFAULT_CHUNK_SIZE = 2000
DEFAULT_OVERLAP = 200


@dataclass(slots=True)
class Chunk:
    chunk_id: int
    text: str
    start: int
    end: int
    word_count: int
    char_count: int
    heading: str | None = None
    heading_level: int = 0
    heading_path: list[str] = field(default_factory=list)


def chunk_text(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP) -> list[Chunk]:
    """Split text into overlapping chunks, breaking at sentence boundaries."""
    text = text.replace("\u00a0", " ")
    if not text.strip():
        return []

    if len(text) <= chunk_size:
        stripped = text.strip()
        return [Chunk(
            chunk_id=1, text=stripped, start=0, end=len(text),
            word_count=len(stripped.split()), char_count=len(text),
        )]

    chunks: list[Chunk] = []
    start = 0
    cid = 1

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Find a sentence boundary to break at
        if end < len(text):
            window = text[max(end - 150, start) : end]
            for sep in (". ", ".\n", "! ", "? ", "\n\n"):
                idx = window.rfind(sep)
                if idx > -1:
                    end = max(end - 150, start) + idx + len(sep)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(Chunk(
                chunk_id=cid, text=chunk, start=start, end=end,
                word_count=len(chunk.split()), char_count=len(chunk),
            ))
            cid += 1

        if end >= len(text):
            break
        start = end - overlap

    return chunks


def _parse_markdown_sections(text: str) -> list[dict]:
    """Parse markdown into sections delimited by ATX headers."""
    header_re = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    matches = list(header_re.finditer(text))

    if not matches:
        return [{"heading": None, "level": 0, "parent": None, "path": [],
                 "text": text, "start": 0, "end": len(text)}]

    sections = []
    stack: list[tuple[int, str]] = []

    # Preamble before first header
    if matches[0].start() > 0:
        pre = text[: matches[0].start()]
        if pre.strip():
            sections.append({"heading": None, "level": 0, "parent": None, "path": [],
                             "text": pre, "start": 0, "end": matches[0].start()})

    for i, m in enumerate(matches):
        level = len(m.group(1))
        heading = m.group(2).strip()
        sec_start = m.start()
        sec_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        while stack and stack[-1][0] >= level:
            stack.pop()

        parent = stack[-1][1] if stack else None
        path = [h for _, h in stack] + [heading]
        stack.append((level, heading))

        sections.append({
            "heading": heading, "level": level, "parent": parent, "path": path,
            "text": text[sec_start:sec_end], "start": sec_start, "end": sec_end,
        })

    return sections


def chunk_markdown(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP) -> list[Chunk]:
    """Split markdown by header boundaries, sub-chunking oversized sections."""
    if not text.strip():
        return []

    sections = _parse_markdown_sections(text)

    if len(sections) == 1 and sections[0]["level"] == 0:
        return chunk_text(text, chunk_size, overlap)

    chunks: list[Chunk] = []
    cid = 1

    for sec in sections:
        sec_text = sec["text"].strip()
        if not sec_text:
            continue

        if len(sec_text) <= chunk_size:
            chunks.append(Chunk(
                chunk_id=cid, text=sec_text, start=sec["start"], end=sec["end"],
                word_count=len(sec_text.split()), char_count=len(sec_text),
                heading=sec["heading"], heading_level=sec["level"], heading_path=sec["path"],
            ))
            cid += 1
        else:
            sub = chunk_text(sec_text, chunk_size, overlap)
            for sc in sub:
                sc.chunk_id = cid
                sc.start += sec["start"]
                sc.end = sc.start + sc.char_count
                sc.heading = sec["heading"]
                sc.heading_level = sec["level"]
                sc.heading_path = sec["path"]
                chunks.append(sc)
                cid += 1

    return chunks


def auto_chunk(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP) -> list[Chunk]:
    """Auto-detect format and chunk accordingly."""
    if re.search(r"^#{1,6}\s+", text, re.MULTILINE):
        return chunk_markdown(text, chunk_size, overlap)
    return chunk_text(text, chunk_size, overlap)
