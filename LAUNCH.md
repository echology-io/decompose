# Decompose — Launch Plan

**"Stop prompting. Start decomposing."**

**Repo:** `echology-io/decompose`
**Site:** echology.io

---

## What Decompose Is

The missing cognitive primitive for AI agents.

Agents fail on complex input because they receive unstructured chaos. Decompose gives any agent the ability to break any input into structured, composable intelligence — instantly. No LLM. No setup. One function call.

**Positioning:** Decompose is not a parser. It's a stability layer for agent reasoning.

**Philosophy:** All intelligence begins with decomposition.

---

## What We're NOT Building

| Temptation | Why No |
|---|---|
| Web service / API | MCP runs locally. Zero ops. |
| Database | Pure function. Stateless. |
| LLM dependency | Kills adoption. Pure Python. Works offline. |
| Config files | Sensible defaults. Env vars for power users. |
| Docker | `pip install decompose`. Done. |
| Auth / accounts | Local tool. No signup. |
| Plugin system | Premature. Hardcode extractors. |
| Multiple formats | JSON only. Agents consume JSON. |

---

## Viral Mechanics

### Agents Are the Customer
OpenClaw users don't discover tools — their agents do. Build for:
- Stateless, fast, deterministic
- Predictable JSON schema
- Easy to chain with other tools
- Idempotent
- Never breaks

Agents promote tools that work. Templates embed tools that are reliable. Forks inherit tools that are standard.

### The Distribution Loop
1. User installs (one line in MCP config)
2. Agent gets measurably better at documents
3. User shares config in community
4. New users install (one line)
5. Templates embed decompose as Step 1
6. Forks inherit it
7. It becomes infrastructure

### Built-In Virality
- Subtle `_decompose` key in output JSON (attribution without noise)
- Composable by design: any agent can wrap it, chain it, extend it

---

## Open Core Strategy

**Open (Proprietary, free to use):** Core decompose engine, MCP server, CLI, all extractors.

**Enterprise (future):** AECai-grade features — jurisdiction crossref, simulation-aware verification (Aletheia), holographic resilience (Daedalus), audit ledger.

Open builds authority. Enterprise preserves monetization. The open tool is the top of the funnel for the full Echology stack.
