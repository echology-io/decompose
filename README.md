# Decompose

[![CI](https://github.com/echology-io/decompose/actions/workflows/ci.yml/badge.svg)](https://github.com/echology-io/decompose/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/decompose-mcp)](https://pypi.org/project/decompose-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/decompose-mcp)](https://pypi.org/project/decompose-mcp/)

<!-- mcp-name: io.github.echology-io/decompose -->

**Stop prompting. Start decomposing.**

The missing cognitive primitive for AI agents. Decompose turns any text into classified, structured semantic units — instantly. No LLM. No setup. One function call.

---

### Before: your agent reads this

```
The contractor shall provide all materials per ASTM C150-20. Maximum load
shall not exceed 500 psf per ASCE 7-22. Notice to proceed within 14 calendar
days of contract execution. Retainage of 10% applies to all payments.
For general background, the project is located in Denver, CO...
```

### After: your agent reads this

```json
[
  {
    "text": "The contractor shall provide all materials per ASTM C150-20.",
    "authority": "mandatory",
    "risk": "compliance",
    "type": "requirement",
    "irreducible": true,
    "attention": 8.0,
    "entities": ["ASTM C150-20"]
  },
  {
    "text": "Maximum load shall not exceed 500 psf per ASCE 7-22.",
    "authority": "prohibitive",
    "risk": "safety_critical",
    "type": "constraint",
    "irreducible": true,
    "attention": 10.0,
    "entities": ["ASCE 7-22"]
  }
]
```

Every unit classified. Every standard extracted. Every risk scored. Your agent knows what matters.

---

## Install

```bash
pip install decompose-mcp
```

## Use as MCP Server

Add to your agent's MCP config (Claude Code, Cursor, Windsurf, etc.):

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

Your agent gets two tools:
- **`decompose_text`** — decompose any text
- **`decompose_url`** — fetch a URL and decompose its content

### OpenClaw

Install the skill from ClawHub or configure directly:

```json
{
  "mcpServers": {
    "decompose": {
      "command": "python3",
      "args": ["-m", "decompose", "--serve"]
    }
  }
}
```

Or install the skill: `clawdhub install decompose-mcp`

## Use as CLI

```bash
# Pipe text
cat spec.txt | decompose --pretty

# Inline
decompose --text "The contractor shall provide all materials per ASTM C150-20."

# Compact output (smaller JSON)
cat document.md | decompose --compact
```

## Use as Library

```python
from decompose import decompose_text

result = decompose_text("The contractor shall provide all materials per ASTM C150-20.")

for unit in result["units"]:
    print(f"[{unit['authority']}] [{unit['risk']}] {unit['text'][:60]}...")
```

---

## What Each Field Means

| Field | Values | What It Tells Your Agent |
|-------|--------|--------------------------|
| `authority` | mandatory, prohibitive, directive, permissive, conditional, informational | Is this a hard requirement or background? |
| `risk` | safety_critical, security, compliance, financial, contractual, advisory, informational | How much does this matter? |
| `type` | requirement, definition, reference, constraint, narrative, data | What kind of content is this? |
| `irreducible` | true/false | Must this be preserved verbatim? |
| `attention` | 0.0 - 10.0 | How much compute should the agent spend here? |
| `entities` | standards, codes, regulations | What formal references are cited? |
| `actionable` | true/false | Does someone need to do something? |

---

## Why No LLM?

Decompose runs on pure regex and heuristics. No Ollama, no API key, no GPU, no inference cost.

This is intentional:
- **Fast**: <500ms for a 50-page spec
- **Deterministic**: Same input always produces same output
- **Offline**: Works air-gapped, on a plane, on CI
- **Composable**: Your agent's LLM reasons over the structured output — decompose handles the preprocessing

The LLM is what *your agent* uses. Decompose makes whatever model you're running work better.

---

## Built by Echology

Decompose is extracted from [AECai](https://aecai.io), a document intelligence platform for Architecture, Engineering, and Construction firms. The classification patterns, entity extraction, and irreducibility detection are battle-tested against thousands of real AEC documents — specs, contracts, RFIs, inspection reports, pay applications.

### Blog

- [When Regex Beats an LLM](https://echology.io/blog/regex-beats-llm) — Decompose classifies the MCP spec in 3.78ms
- [Why Your Agent Needs a Cognitive Primitive](https://echology.io/blog/cognitive-primitive) — attention scoring, irreducibility, and routing
- [What "Simulation-Aware" Actually Means](https://echology.io/blog/simulation-aware) — the architecture behind AECai

**License:** Proprietary — Copyright (c) 2025-2026 Echology, Inc.

**Philosophy:** All intelligence begins with decomposition.
