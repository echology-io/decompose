# Decompose — Human Required Tasks

Everything in this file requires Kyle with credentials, a browser, or a human judgment call. Ordered by priority and grouped by phase.

---

## Phase 1: Ship (Days 1-3)

### GitHub
- [x] `cd /Users/kylevines/echology && git init && git add -A && git commit -m "Initial commit: decompose v0.1.0"`
- [x] `gh repo create echology-io/decompose --public --source . --push`
- [ ] Add repo description: "Stop prompting. Start decomposing. Structured intelligence for AI agents."
- [ ] Add topics: `mcp`, `ai-agents`, `decompose`, `semantic`, `structured-data`, `document-intelligence`

### PyPI
- [ ] Create account at pypi.org (if needed)
- [ ] Generate API token scoped to `decompose` package
- [ ] Add as GitHub secret: Settings > Secrets > `PYPI_API_TOKEN`
- [ ] Tag and push: `git tag v0.1.0 && git push --tags` (triggers publish workflow)
- [ ] Verify `pip install decompose` works from PyPI

### Domain (Optional, High-Value)
- [ ] Check Namecheap for `decompose.new` availability
- [ ] If unavailable: `decompose.dev`, `decompose.sh`, or just use `echology.io/decompose`
- [ ] Point `echology.io` DNS to GitHub Pages (CNAME record)

---

## Phase 2: Distribute (Days 4-10)

### The "Whoa" Demo
This is the single most important marketing asset. Everything else amplifies this.

- [ ] Pick a real 30-50 page AEC spec (you have plenty in data/outputs)
- [ ] Screen record terminal session:
  1. `cat big_spec.txt | wc -l` — show it's huge
  2. `cat big_spec.txt | decompose --pretty | head -80` — show structured output
  3. Show the meta summary: X units, Y standards found, Z% safety_critical
  4. Feed decomposed output to an agent, watch it reason cleanly
- [ ] Cut to 60 seconds max
- [ ] Export as GIF (for README) and MP4 (for social)
- [ ] Add GIF to README.md hero section

### OpenClaw Integration
- [ ] Find OpenClaw's AgentSkill registry / community marketplace
- [ ] Submit decompose as a skill with this config:
  ```json
  {"mcpServers": {"decompose": {"command": "uvx", "args": ["decompose", "--serve"]}}}
  ```
- [ ] Write a 3-sentence skill description using the positioning: "The missing cognitive primitive for agents"
- [ ] Include before/after example in the listing

### Seed the Builder Network
- [ ] Identify 5-10 active OpenClaw builders (GitHub contributors, Discord active members)
- [ ] DM each one. Template:
  > "Hey — I built an MCP tool called Decompose that gives agents structured intelligence from documents. No LLM needed, <500ms. Would love your take. [repo link]"
- [ ] Offer: early access to roadmap, feature priority for their use cases, co-marketing

---

## Phase 3: Amplify (Days 10-21)

### X / Twitter
- [ ] Thread format (3-5 tweets):
  1. "Stop prompting. Start decomposing." + 30s demo clip
  2. Before/after screenshot (raw text vs structured JSON)
  3. "No LLM. No API key. No GPU. Pure Python. <500ms."
  4. "Install: `uvx decompose`. One line. Works with any model."
  5. Link to repo
- [ ] Tag: @OpenClaw, any builder allies from Phase 2, @echaborations (your account)

### LinkedIn
- [ ] Post framing: "We just gave AI agents the ability to understand complex documents."
- [ ] Lean on your AEC credibility — this isn't a toy, it's extracted from production
- [ ] Include the 60s demo video
- [ ] Target connections in: AEC tech, AI/ML engineering, developer tools

### Reddit
- [ ] r/LocalLLaMA — "I built an MCP tool that makes local models better at documents (no LLM needed, pure regex)"
- [ ] r/AItools — "Decompose: structured intelligence for AI agents"
- [ ] Post the build breakdown: what it does, how it works, why no LLM, benchmarks
- [ ] Engage comments. Answer every question within 24 hours.

### Hacker News
- [ ] Show HN title: "Decompose: The missing cognitive primitive for AI agents (MCP, no LLM)"
- [ ] Time: Tuesday or Wednesday, 8-10am ET
- [ ] Be ready to answer comments for 6+ hours straight
- [ ] Have benchmarks ready: processing speed, token reduction, accuracy against labeled data

### Blog Post
- [ ] Title: "Why Agents Fail Without Decomposition"
- [ ] Publish on: Medium, Dev.to, or echology.io/blog
- [ ] Structure: Problem (agents choke on long docs) → Insight (they need structure, not more tokens) → Solution (decompose) → Benchmarks → Install
- [ ] Cross-link from README

---

## Phase 4: Sustain (Week 3-4+)

### Community
- [ ] Monitor GitHub Issues — respond within 24 hours
- [ ] Accept PRs that add entity patterns or fix edge cases
- [ ] Ship v0.2.0 based on feedback from Phase 2-3

### Templates
- [ ] Create 3 agent workflow templates (separate repos or gists):
  1. **Decompose → Plan → Execute** — Document review workflow
  2. **Decompose → Verify → Generate** — Compliance checking
  3. **Decompose → Search → Report** — Knowledge retrieval
- [ ] Each template should be forkable in 30 seconds

### Metrics to Track
- [ ] GitHub stars (target: 100 in week 1, 500 by month 1)
- [ ] PyPI downloads (target: 1k in month 1)
- [ ] OpenClaw skill installs
- [ ] Issues/PRs from external contributors

---

## Recurring (Weekly)
- [ ] Check PyPI download stats
- [ ] Respond to GitHub issues
- [ ] Post one piece of content (tweet, short-form, comment on related thread)
- [ ] DM 2-3 new builders in the agent ecosystem
