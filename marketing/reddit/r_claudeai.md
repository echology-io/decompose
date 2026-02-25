# r/ClaudeAI

**Flair:** MCP

**Title:** (99 chars)
```
I built an MCP server that classifies documents in ~14ms with zero API calls — pure regex, no LLM
```

---

**Body:**

If your Claude workflow involves reading specs, contracts, or technical documents, Decompose can pre-classify the content so Claude knows what matters before it starts reading.

It's an MCP server with two tools:
- `decompose_text` — classify any text into semantic units
- `decompose_url` — fetch a URL and classify its content

Each unit gets: authority level, risk category, attention score (0-10), entity list, and an irreducibility flag.

Add to your MCP config (Claude Desktop, Cursor, Claude Code, etc.):

```json
{
  "mcpServers": {
    "decompose": {
      "command": "python",
      "args": ["-m", "decompose", "--serve"]
    }
  }
}
```

Or with uvx (no install needed):

```json
{
  "mcpServers": {
    "decompose": {
      "command": "uvx",
      "args": ["decompose-mcp", "--serve"]
    }
  }
}
```

No API key. No cloud. Runs locally in ~14ms per document. Listed on the official MCP Registry.

I tested it against the Anthropic prompt engineering docs — 10 pages, 43 semantic units, 34ms total. The financial analysis example correctly flagged as irreducible (PRESERVE_VERBATIM) with all dollar amounts extracted. The MCP Transport spec's security warning scored 4.5/10 attention while the overview scored 0.0.

GitHub: https://github.com/echology-io/decompose
PyPI: pip install decompose-mcp

**What you do after classification:** Filter by attention score to decide what Claude reads first. Route safety-critical units to one prompt, financial to another, skip boilerplate entirely. Use the irreducibility flag to protect content Claude must not paraphrase. Runnable examples in the `examples/` directory.

Built by Echology — extracted from AECai, a document intelligence platform for architecture/engineering/construction firms.
