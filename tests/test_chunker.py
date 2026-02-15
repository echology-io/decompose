"""Tests for decompose.chunker."""

from decompose.chunker import auto_chunk, chunk_markdown, chunk_text


class TestChunkText:
    def test_empty_returns_empty(self):
        assert chunk_text("") == []
        assert chunk_text("   ") == []

    def test_small_text_single_chunk(self):
        chunks = chunk_text("Hello world.", chunk_size=100)
        assert len(chunks) == 1
        assert chunks[0].text == "Hello world."
        assert chunks[0].chunk_id == 1

    def test_large_text_splits(self):
        text = "This is a sentence. " * 200  # ~4000 chars
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        assert len(chunks) > 1
        # All chunks should have content
        for c in chunks:
            assert c.text.strip()
            assert c.word_count > 0

    def test_overlap_creates_shared_content(self):
        text = "Word " * 1000
        chunks = chunk_text(text, chunk_size=200, overlap=50)
        assert len(chunks) > 1


class TestChunkMarkdown:
    def test_splits_by_headers(self):
        md = "# Section 1\nContent one.\n# Section 2\nContent two."
        chunks = chunk_markdown(md)
        assert len(chunks) == 2
        assert chunks[0].heading == "Section 1"
        assert chunks[1].heading == "Section 2"

    def test_heading_path_tracks_hierarchy(self):
        md = "# Top\n## Sub\nContent here."
        chunks = chunk_markdown(md)
        sub = [c for c in chunks if c.heading == "Sub"]
        assert len(sub) == 1
        assert sub[0].heading_path == ["Top", "Sub"]

    def test_no_headers_falls_back(self):
        text = "Just plain text with no markdown headers."
        chunks = chunk_markdown(text)
        assert len(chunks) == 1
        assert chunks[0].heading is None

    def test_preamble_before_headers(self):
        md = "Preamble text.\n# First\nContent."
        chunks = chunk_markdown(md)
        assert chunks[0].heading is None
        assert "Preamble" in chunks[0].text


class TestAutoChunk:
    def test_detects_markdown(self):
        md = "# Title\nBody text."
        chunks = auto_chunk(md)
        assert chunks[0].heading == "Title"

    def test_falls_back_to_text(self):
        plain = "No headers here. Just sentences."
        chunks = auto_chunk(plain)
        assert chunks[0].heading is None
