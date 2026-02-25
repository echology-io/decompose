# Echology — Complete Operating Document

**Version:** 1.0 | **Last updated:** 2026-02-21
**Purpose:** Single source of truth. Use as LLM system context (Claude, Ollama), Notion wiki page, and accountability roadmap.

---

## 1. Company

**Echology, Inc.** — Delaware C-Corp, operating in South Carolina. EIN obtained. Insurance pending.

Practitioner-built tools that empower engineering firms to take positive action with AI. Not an AI agency, not a prompt shop, not a research lab. Tools emerge from doing the work.

**Website:** https://echology.io (GitHub Pages, bilingual EN + PT)
**Domains:** echology.io, aecai.io, kylevines.com

---

## 2. Founder

**Kyle Vines** — Solo technical founder/CEO. 13+ years geotechnical/civil engineering. Acquired and ran a geotech firm. Last role: LaBella Associates (ENR Top 200) — adopted AI tools, validated them across 200 engineers, tools stuck. He was cut out after deployment. Charleston, SC, three kids. 19,000+ lines of production code, solo. Mother is CTO and cybersecurity board member — security in DNA, not bolted on.

Kyle is not bitter about the ENR 200 experience. He appreciates the lessons learned and builds from clarity, not resentment.

**Core thesis:** "I adopted AI inside an engineering firm and it worked. Now I'm packaging those lessons so other firms can do the same."

---

## 3. Origin Story

- Kyle worked in engineering for 13+ years, adopted AI tools practically
- Applied tools at an ENR Top 200 firm — they were adopted, they stuck
- Kyle was cut out after deployment
- While building Echo (the tooling), interesting ideas emerged from the work itself
- Launched Echology to take ALL lessons learned across ALL experience and empower firms to take positive action
- Echology exists so Kyle owns the platform, the IP, and the relationship — not someone else
- Credibility is practitioner-first: industry person who found what works, not researcher who found an industry

---

## 4. Identity

**What Echology IS:** Practitioner-built tools that empower engineering firms to take positive action with AI.

**What Echology is NOT:** AI agency, prompt shop, theoretical research lab, SaaS vendor.

**Company architecture:**
```
Echology (lessons learned -> tools -> empowerment for firms)
  -> AECai (the platform — engineering experience encoded into systems)
  -> Toolbox (Decompose, validators, escalation patterns, provenance)
  -> Tools that prove worthy get released standalone
```

**Through-line:**
- Practitioner experience decides what to build — tools emerge from doing the work
- Ideas came from building, not before it — SimArch, Decompose, the pipeline patterns all emerged from practice
- AECai encodes operational knowledge, not just code
- Tools that prove themselves get extracted and released (Decompose was the first)
- The same patterns keep working in different domains — that's resonance from real application

---

## 5. Tone and Language

**Voice:** Controlled, technical, deliberate, slightly austere. Engineer-to-engineer, peer not vendor.

**Use:**
- "Building tools that think in structure" (tagline)
- "Modernizing technology to optimize workflows, where it makes sense"
- "I adopted AI inside an engineering firm and it worked"
- Ground in practitioner credibility, not abstract thesis

**Never use:**
- "AI for AEC" — this is about empowering firms with lessons learned
- "Revolutionary", "game-changing", "excited to announce"
- Cheerful, playful, startup-ish, friendly SaaS tone

**Key framing:**
- Decompose is "a tool that earned its independence" — not the thesis
- The thesis is Kyle's experience, not any single tool or paper
- AEC is the first domain, not the only domain
- Experience first, tools second, standalone releases when earned
- Never fabricate Kyle's narrative — ground in his words, not inferred thesis

---

## 6. Business Model

### Phase 1 (now): Consulting

Modernize technology to optimize workflows for engineering firms, where it makes sense. Consulting is the vehicle to prove the platform, generate revenue, and refine tools from real use.

**Positioning:** "I'm an engineer-turned-consultant who happens to build AI tools" — peer, not vendor.

### Phase 2 (earned): Platform

Platform stands on its own. Consulting becomes optional/premium. Earned through successful engagements and proven ROI.

### Pricing Tiers

| Tier | Price | Details |
|------|-------|---------|
| Discovery Assessment | $800 (immediate booking) / $1,000 standard | 2-week delivery. Credit card, no PO. Below procurement threshold. Credits 100% toward full engagement. |
| SaaS Subscription | $5K-$15K/month per firm | Monthly. |
| Enterprise | $100K-$250K/year | Multi-office firms. Annual. |

Cost per client after onboarding: ~$0 (no cloud compute, no API fees). Gross margins >90%.

**TAM:** Top 500 ENR firms x $10K/month avg = $60M ARR from Tier 1 alone. Thousands more mid-market firms below that.

### Product Roles

- **Decompose** = open-source credibility builder, teaching tool, supports consulting conversations
- **AECai** = proprietary platform, the engine behind engagements
- **SimArch** = internal IP only, not marketed externally

---

## 7. Competitive Moat (5 layers)

1. **Air-gapped architecture** — Only local-first product. Competitors require cloud. Engineering firms with NDA-protected data won't accept cloud. Non-negotiable.
2. **Jurisdiction code registry** — Structured data on which AHJ adopted which code edition with amendments. Doesn't exist elsewhere in queryable form. 500+ code bodies seeded.
3. **Domain-specific AI** — Understands ASCE 7, ACI 318, OSHA 29 CFR 1926, inter-entity relationships. Not generic document AI. 62 AEC keywords, 60+ doc type signatures.
4. **Consulting-first positioning** — $800 assessment removes procurement friction, proves value before software commitment.
5. **Founder domain expertise** — 13 years in engineering = instant credibility with buyers.

---

## AECai Platform

See [aecai/AECAI.md](../aecai/AECAI.md) for the complete AECai platform architecture, including:
- Vanta Engine (document processing pipeline)
- Aletheia (verification & compliance)
- Daedalus (retrieval & automation)
- Temporal workflows & API reference
- Configuration & deployment

---

## 8. Sales Strategy

### Ideal Customer Profile

**Firmographics:** ENR Top 500, 50+ engineers, civil/structural/geotech/environmental, $50M+ revenue.

**Buyer personas (authority order):**
1. VP of Engineering / Chief Engineer
2. Director of Operations
3. Principal / Associate Principal
4. CTO / Director of Innovation
5. Regional Director

**Anti-targets:** Under 30 engineers, pure architecture, construction-only GCs, existing competitor relationships.

### Outbound Phases

1. **Warm Intros** — 30+ mapped names, highest conversion
2. **LinkedIn** — 3-day engagement ritual, then DM
3. **Email Sequences** — Plain text, max 150 words, Tue-Thu 7-9 AM
4. **Phone** — Follow-up only (email opened 2+ times, no reply)
5. **Discovery Call** — 15-20 min: discover → bridge → $800 assessment offer

### 30-60-90 Day Targets

| Window | Targets |
|--------|---------|
| Days 1-30 | 20 warm intros, 2-3 paid assessments |
| Days 31-60 | 5-7 total assessments, 1-2 full engagements in pipeline |
| Days 61-90 | 4-6 assessments/month, first full engagement, $50K-$100K pipeline |

---

## 9. Marketing Agent

**Location:** `marketing/` (tracked in this repo)

Automated content generation system. Detects shipping events (GitHub releases/tags), generates blog posts (EN + PT) and LinkedIn drafts using Claude CLI.

**Channels:** blog (EN), blog_pt (PT), linkedin
**Voice:** First-person as Kyle, engineer-to-engineer, practitioner-first positioning
**Style guide:** `marketing/voice_corpus/style_guide.md`

---

## 10. Current State

**Entity status:** Delaware C-Corp formed. EIN obtained. Operating in SC. Insurance pending.

**Products:**
- AECai v3.1.0 — 577 tests passing (see `~/aecai/AECAI.md`)
- Decompose v0.2.0 — 76 tests passing
- RBS Policy QC — live at echology.io/rbs

---

## 11. Repository Structure

```
Echology, Inc.
├── echology/          → github.com/echology-io/decompose
│   ├── src/decompose/   Decompose library (PyPI: decompose-mcp v0.2.0)
│   ├── tests/           76 tests
│   ├── docs/            GitHub Pages → echology.io
│   └── marketing/       Marketing agent (tracked)
│
├── aecai/             → github.com/echology-io/aecai (private)
│   ├── engine/          Vanta, Aletheia, Daedalus
│   ├── training/        MLX fine-tuning
│   ├── ops/sops/        Product SOPs, deployment guides
│   ├── temporal/        6 workflows, 18 activities
│   └── tests/           577 tests
│
└── rbs-demo/          → github.com/echology-io/rbs-demo (private)
    ├── server.py        FastAPI extraction engine
    └── index.html       Frontend SPA
```

---

## 12. Roadmap

### Immediate
- [ ] SC foreign qualification filed
- [ ] Business insurance (liability, cyber, E&O)
- [ ] Activate outbound sales (warm intros → LinkedIn → email sequences)
- [ ] Book first paid assessments ($800)

### 30-90 Days
- [ ] Deliver first assessments, collect testimonials
- [ ] Close first full engagement ($15K-$75K)
- [ ] Publish first case study
- [ ] Reach $50K-$100K pipeline

### Future (earned)
- [ ] Gen 2.0: PostgreSQL, JWT/RBAC, multi-tenancy
- [ ] Platform self-serve (consulting becomes optional)
- [ ] Procore/ACC integration

---

## 13. Risk to Watch

- Drifting into abstraction without tangible deployed systems
- Becoming a research lab instead of shipping vertical systems with real metrics
- Letting tools overshadow the practitioner story in positioning
- Building product features speculatively before user/client feedback
- Over-engineering Gen 2.0 features before consulting revenue validates direction

---

## 14. Notion Integration

**Tasks: Workflow DB:** `collection://2682973f-06dc-8190-aa33-000bef5503cd`
**DB URL:** `https://www.notion.so/2682973f06dc8115b832efbe10cf82ef`

**Sync protocol:** Edit `TASKS.md` locally → batch-sync via `notion-update-page` MCP tool. Notion is source of truth.

---

## 15. Infrastructure

**Hardware:** Mac Mini M4 Pro, 8-core, 16GB RAM, 512GB internal SSD
**Storage:** echo_dev (1TB external SSD), echo_backup (1.8TB external HDD)
**System Python:** 3.9.6 — always use .venv with Python 3.11
