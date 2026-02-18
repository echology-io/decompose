# When Your AI Can't Explain Why It Flagged a Document

A contractor submits a 47-page structural specification. Your AI pipeline ingests it, splits it into sections, and flags three of them as safety-critical. The project manager asks: "Why those three?"

If your classification layer is an LLM, the honest answer is: "The model thought so." Run it again tomorrow — you might get four flags, or two, with different sections. The output is non-deterministic. The reasoning is opaque. And in an industry where wrong classifications carry professional liability, that's not engineering. That's a coin flip.

This is the problem Decompose solves. And in v0.1.1, it now solves a piece that was missing: security classification.

## What shipped in v0.1.1

Decompose v0.1.1 adds a `security` risk category to classification output. Every semantic unit now gets evaluated for security-relevant content — authentication requirements, access control specifications, encryption mandates, credential handling — alongside the existing authority levels, risk scores, and entity extraction.

The classification is deterministic. Same input, same output, every time. No LLM, no API key, no GPU. One function call.

```python
from decompose import decompose_text

result = decompose_text("""
All API endpoints MUST require Bearer token authentication.
Credentials MUST NOT be logged or stored in plaintext.
The system SHOULD support rate limiting for public endpoints.
""")

for unit in result["units"]:
    print(f"[{unit['classification']}] risk={unit['risk_score']} security={unit.get('security', False)}")
    print(f"  {unit['text'][:80]}")
```

The output is structured JSON. Every unit gets a classification, a risk score, extracted entities, and now a security flag. You can filter, sort, route, and audit every decision your pipeline makes — because every decision is a deterministic function of the input text.

## What this looks like in practice

Here's a real decomposition of the MCP Transport Specification. Before v0.1.1, you'd get authority levels and risk scores. Now you also get security classification:

```
[mandatory]  risk=0.85  security=true   "Implementations MUST validate authentication tokens..."
[mandatory]  risk=0.70  security=false  "The server MUST respond within 30 seconds..."
[advisory]   risk=0.30  security=false  "Implementations SHOULD support batch requests..."
[info]       risk=0.00  security=false  "This section describes the transport layer..."
```

The security flag catches authentication requirements, access control language, credential handling instructions, and encryption mandates. It uses pattern matching against RFC 2119 keywords combined with security-domain vocabulary — not statistical inference.

An LLM can do this classification too. It will take 2-10 seconds, cost $0.003-0.02 per call, and give you slightly different answers each run. Decompose does it in single-digit milliseconds. Deterministically. Offline. For free.

## What it cannot do

Decompose doesn't understand context. It doesn't know that a 4,000 psf bearing capacity is unusual for clay soil, or that a particular authentication scheme is outdated, or that two sections of a spec contradict each other. It performs mechanical classification — splitting, scoring, extracting, flagging — based on linguistic patterns.

This is the point. Your LLM handles nuance, cross-referencing, intent, and domain reasoning. Decompose handles the structural work so the LLM can focus on what it's actually good at. You get a deterministic scaffold that your probabilistic model can reason over — and every classification in that scaffold is auditable, reproducible, and explainable.

## Why this matters beyond a feature flag

If your AI system processes documents and someone asks "why did it flag this section as security-critical?" — you need a real answer. "The model said so" doesn't hold up in construction. It doesn't hold up in healthcare. It doesn't hold up in any industry where documents have legal weight.

Decompose gives you that answer. The classification is a function of the input text. You can trace every flag back to the pattern that triggered it. You can write tests against it. You can version it, diff it, and reproduce it a year from now on the same input and get the same output.

Determinism isn't a limitation. It's the foundation that makes everything above it trustworthy.

## Also in this release

- Published to the ClawHub marketplace — install via OpenClaw or the ClawHub registry
- Added CONTRIBUTING.md and LICENSE (BSD-3-Clause) for open-source contributors
- Open Graph and Twitter Card meta tags across all echology.io pages
- Updated README with blog post links and ClawHub install instructions
- 31 commits across 44 files

## Try it

```bash
pip install decompose-mcp==0.1.1
```

Or add it as an MCP server for Claude, Cursor, or any MCP-compatible client:

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

Source: [github.com/echology-io/decompose](https://github.com/echology-io/decompose)
Docs: [echology.io/decompose](https://echology.io/decompose)