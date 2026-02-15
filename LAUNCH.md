# Decompose — Launch Plan

**"Stop prompting. Start decomposing."**

**Owner:** Kyle Vines / Echology, Inc.
**Repo:** `echology-io/decompose`
**Domain:** echology.io (Namecheap)

---

## What Decompose Is

The missing cognitive primitive for AI agents.

Agents fail on complex input because they receive unstructured chaos. Decompose gives any agent the ability to break any input into structured, composable intelligence — instantly. No LLM. No setup. One function call.

**Positioning:** Decompose is not a parser. It's a stability layer for agent reasoning.

**Philosophy:** All intelligence begins with decomposition.

**Stack alignment:**
- Vanta reads
- **Decompose structures**
- Aletheia verifies
- Daedalus generates

---

## You (Physical / Manual)

These require a human with credentials. Cannot be automated.

### Accounts & Credentials (30 min)
- [ ] **PyPI account** — pypi.org. Generate API token scoped to `decompose` package
- [ ] **decompose.new domain** — Check Namecheap. High-value if available. Fallback: `echology.io/decompose`
- [ ] **echology.io DNS** — CNAME to GitHub Pages for landing page

### GitHub Setup (10 min)
- [x] **Init remote** — `gh repo create echology-io/decompose --public --source . --push`
- [ ] **Add secret** — Settings > Secrets > `PYPI_API_TOKEN`
- [ ] **Enable Pages** — Settings > Pages > `gh-pages` branch

### The "Whoa" Demo (1 hour)
This is the most important thing you do. Everything else is mechanics.

- [ ] **Record 60-second demo** — Screen capture showing:
  1. Paste a 40-page AEC spec into terminal
  2. Run `decompose`
  3. Show structured JSON tree: sections, entities, constraints, risk flags
  4. Feed that output into an agent (OpenClaw or Claude Code)
  5. Agent reasons flawlessly over the structured input
  6. The visible jump from confusion to clarity = viral moment
- [ ] **Convert to GIF** for README hero image
- [ ] **It must look like magic**

### Distribution Push (Week 1-2)
- [ ] **5 OpenClaw builders** — DM directly. Offer early access, feature priority, co-marketing. Make them insiders. They embed it into their agents.
- [ ] **OpenClaw AgentSkill submission** — Register `decompose` as a preconfigured MCP skill in their registry
- [ ] **X/Twitter thread** — 30-second Loom + 3 examples + "Fork here" link. Tag OpenClaw. "Stop prompting. Start decomposing."
- [ ] **LinkedIn** — "We just gave AI agents the ability to understand complex documents." You have AEC + AI credibility. Use it.
- [ ] **Reddit** — r/LocalLLaMA, r/AItools. Post the build breakdown with benchmarks
- [ ] **Hacker News** — Show HN: "Decompose: Structured intelligence for AI agents (MCP, no LLM)" — post when metrics are solid
- [ ] **Blog post** — "Why Agents Fail Without Decomposition" — technical, with benchmarks

### Distribution Templates (Week 2-3)
- [ ] **"Decompose → Plan → Execute"** agent template
- [ ] **"Decompose → Verify → Generate"** agent template
- [ ] **"Decompose → Train → Retrieve"** agent template
- [ ] Make Decompose the entry point of every template. Infrastructure spreads through reuse.

---

## Automated (Claude Builds Now)

### Project Scaffold
- [ ] `pyproject.toml` — uv/pip, `[project.scripts]`, MCP entrypoint for uvx
- [ ] `src/decompose/` — src layout, `py.typed`
- [ ] `LICENSE` — MIT
- [ ] `.github/workflows/ci.yml` — ruff + pytest on push
- [ ] `.github/workflows/publish.yml` — PyPI on tag
- [ ] `ruff.toml`
- [ ] `.gitignore`

### Core Engine
- [ ] `src/decompose/core.py` — `decompose()`: text in, structured units out
- [ ] `src/decompose/chunker.py` — Header-aware Markdown + semantic chunking
- [ ] `src/decompose/classifier.py` — Authority, risk, content type scoring
- [ ] `src/decompose/irreducibility.py` — Verbatim preservation detection
- [ ] `src/decompose/attention.py` — Attention budget per unit
- [ ] `src/decompose/entities.py` — Standards, dates, parties, financial extraction
- [ ] `src/decompose/types.py` — Pydantic models: `Unit`, `DecomposeResult`

### MCP Server
- [ ] `src/decompose/mcp_server.py` — `decompose_text`, `decompose_url`
- [ ] Stdio transport, JSON output, deterministic schema

### CLI
- [ ] `src/decompose/cli.py` — `decompose < file.txt`, stdout JSON, pipeable

### Tests
- [ ] `tests/test_chunker.py`
- [ ] `tests/test_classifier.py`
- [ ] `tests/test_irreducibility.py`
- [ ] `tests/test_core.py`
- [ ] `tests/test_mcp.py`

---

## What We're NOT Building

| Temptation | Why No |
|---|---|
| Web service / API | MCP runs locally. Zero ops. |
| Database | Pure function. Stateless. |
| LLM dependency | Kills adoption. Pure Python. Works offline. |
| Config files | Sensible defaults. Env vars for power users. |
| Docker | `uvx decompose`. Done. |
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
3. User shares config in OpenClaw community
4. New users install (one line)
5. Templates embed decompose as Step 1
6. Forks inherit it
7. It becomes infrastructure

### Metrics That Spread
Engineers don't share vibes. They share performance:
- **Token reduction**: 78% fewer tokens vs raw text
- **Structured units**: 47 classified units from a 50-page spec
- **Processing time**: <500ms, no LLM
- **Accuracy**: Authority/risk classification benchmarked against human labels
- **Before/after**: Agent task success rate with and without decompose

### Built-In Virality
- Subtle `_decompose` key in output JSON (attribution without noise)
- Template packs: "10 agent workflows powered by Decompose"
- Composable by design: any agent can wrap it, chain it, extend it

---

## The README Hook

```
Stop prompting. Start decomposing.

# Before: your agent reads this
"The contractor shall provide all materials per ASTM C150-20. Maximum load
shall not exceed 500 psf per ASCE 7-22. Notice to proceed within 14 calendar
days of contract execution..."

# After: your agent reads this
[
  {"text": "The contractor shall provide all materials per ASTM C150-20",
   "authority": "mandatory", "risk": "compliance", "type": "requirement",
   "entities": ["ASTM C150-20"], "irreducible": true, "attention": 8.2},
  ...
]

Install:
  uvx decompose

One line. Zero config. No LLM. Works with any model.
```

---

## Open Core Strategy

**Open (MIT):** Core decompose engine, MCP server, CLI, all extractors.

**Enterprise (future):** AECai-grade features — jurisdiction crossref, simulation-aware verification (Aletheia), holographic resilience (Daedalus), audit ledger.

Open builds authority. Enterprise preserves monetization. The open tool is the top of the funnel for the full Echology stack.

---

## 4-Week Sprint

| Week | Focus | Output |
|---|---|---|
| 1 | Build + ship | Working MCP server on PyPI. README with demo GIF. |
| 2 | Distribute | OpenClaw skill submission. X thread. 5 builder DMs. |
| 3 | Templates | 3 agent workflow templates. Blog post with benchmarks. |
| 4 | Amplify | Reddit/HN launch. Community workflows. v1.1 with improvements from feedback. |
