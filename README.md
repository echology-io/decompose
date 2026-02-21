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
from decompose import decompose_text, filter_for_llm

result = decompose_text("The contractor shall provide all materials per ASTM C150-20.")

for unit in result["units"]:
    print(f"[{unit['authority']}] [{unit['risk']}] {unit['text'][:60]}...")

# Pre-filter for LLM context — keep only high-value units
filtered = filter_for_llm(result, max_tokens=4000)
print(f"{filtered['meta']['reduction_pct']}% token reduction")
llm_input = filtered["text"]  # Ready for your LLM
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

## What to Build With This

Decompose is not the destination. It's the step before the LLM that most developers skip — not because it's hard, but because nobody showed them it exists. Documents have structure. That structure is classifiable. And classification should happen before reasoning.

```
Without:  document → chunk → embed → retrieve → LLM → answer  (100% of tokens)
With:     document → decompose → filter/route → LLM → answer  (20-40% of tokens)
```

### Filter: built-in LLM pre-filter

`filter_for_llm()` keeps mandatory, safety-critical, financial, and compliance units — drops boilerplate before it reaches your LLM or vector store.

```python
from decompose import decompose_text, filter_for_llm

result = decompose_text(open("contract.md").read())
filtered = filter_for_llm(result, max_tokens=4000)

# filtered["text"] = high-value units only, ready for LLM
# filtered["meta"]["reduction_pct"] = how much was dropped (typically 60-80%)

# Or use the units directly for embedding
for unit in filtered["units"]:
    embed_and_store(unit["text"], metadata={
        "authority": unit["authority"],
        "risk": unit["risk"],
        "attention": unit["attention"],
    })
```

### Route: risk-based processing

Safety-critical content goes to one chain. Financial content goes to another. Boilerplate gets skipped.

```python
from decompose import decompose_text

result = decompose_text(spec_text)

for unit in result["units"]:
    if unit["risk"] == "safety_critical":
        safety_chain.process(unit)       # Full analysis + human review
    elif unit["risk"] == "financial":
        audit_chain.process(unit)         # Flag for finance team
    elif unit["attention"] < 0.5:
        pass                              # Skip boilerplate
    else:
        general_chain.process(unit)       # Standard LLM analysis
```

### Measure: token cost reduction

```python
from decompose import decompose_text

result = decompose_text(spec_text)
total = len(result["units"])
high = [u for u in result["units"] if u["attention"] >= 1.0]

print(f"{len(high)}/{total} units need LLM analysis")
print(f"{100 - len(high) * 100 // total}% token reduction")
```

See [`examples/`](examples/) for runnable scripts.

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

Free, MIT-licensed, and designed as the on-ramp to understanding document intelligence architecture.

### Blog

- [When Regex Beats an LLM](https://echology.io/blog/regex-beats-llm) — Decompose classifies the MCP spec in 3.78ms
- [Why Your Agent Needs a Cognitive Primitive](https://echology.io/blog/cognitive-primitive) — attention scoring, irreducibility, and routing
- [What "Simulation-Aware" Actually Means](https://echology.io/blog/simulation-aware) — the architecture behind AECai

**License:** MIT — Copyright (c) 2025-2026 Echology, Inc.

**Philosophy:** All intelligence begins with decomposition.
