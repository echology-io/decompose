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

## 18. Sales Strategy

### Ideal Customer Profile

**Firmographics:** ENR Top 500, 50+ engineers, civil/structural/geotech/environmental, $50M+ revenue.

**Buyer personas (authority order):**
1. VP of Engineering / Chief Engineer
2. Director of Operations
3. Principal / Associate Principal
4. CTO / Director of Innovation
5. Regional Director

**Buying signals (pursue if 2+ present):**
- Hiring "Document Control Manager" or "Knowledge Management"
- Senior engineer (20+ years) recently retired/departed
- Won large new contract ($50M+)
- "Digital transformation" or "AI adoption" in company news
- Failed audit or compliance issue
- Rapid headcount growth (10%+ past year)
- Multiple offices / geographic expansion
- Active on Procore, Bluebeam, ProjectWise

**Anti-targets:** Under 30 engineers, pure architecture, construction-only GCs, existing competitor relationships, IT Directors without engineering background.

### Outbound Sales Phases

**Phase 1 — Warm Intros** (highest priority, 3-5x conversion):
- 30+ mapped names (former colleagues, ASCE contacts, subs, vendors)
- 5-8 warm intros/day, Days 3-5

**Phase 2 — LinkedIn:**
- 3-day engagement ritual (like/comment before messaging)
- Day 5 opening: reference specific firm news, no pitch, ask for 15-minute call
- Follow-ups Days 4, 9, 16 with new angles, then break-up
- Content: 3x/week posts (the Dave Story, the Page 247 Story, vulnerability stories)

**Phase 3 — Email Sequences:**
- Sequence A: Connection -> engagement -> opening -> follow-ups (5-7 days)
- Sequence B: Buying signal trigger ("I saw you're hiring a Doc Control Manager")
- Sequence C: Retirement trigger ("When a 30-year engineer walks out the door...")
- Rules: Plain text only, max 150 words, lowercase subject (max 6 words), Tue-Thu 7-9 AM, 5-8/day max

**Phase 4 — Phone** (follow-up only, not cold):
- After email opened 2+ times but no reply
- After discovery call stall
- To confirm assessment booking

**Phase 5 — Discovery Call** (15-20 min):
- Open (2 min): Focus on their situation
- Discover (8-10 min): How many projects? Who reviews specs? How long? Lost senior people? Where do juniors search? Biggest bottleneck? Tried AI? Cloud stance?
- Bridge (2 min): "What you're describing is exactly what we see at most firms"
- Offer (3 min): Assessment pitch — $800 this week, credits 100% toward engagement

### 30-60-90 Day Targets

| Window | Targets |
|--------|---------|
| Days 1-30 | 20 warm intros, 30 qualified prospects, 2-3 discovery calls. **2-3 paid assessments ($1,600-$2,400)** |
| Days 31-60 | 3-4 new assessments, deliver first assessments, collect testimonials. **5-7 total, 1-2 full engagements in pipeline** |
| Days 61-90 | 4-6 assessments/month, first full engagement closed, case study. **$50K-$100K pipeline, 2-3 active clients** |

### Utility-Specific Strategy

**Why utilities:** Massive doc burden (single transmission project = 10,000+ pages), NERC CIP = air-gap non-negotiable, 40-50% workforce retirement-eligible in 5-10 years, billions in grid modernization budgets.

**Tier 1 targets:** Southern Company, Duke Energy, NextEra, Dominion, Xcel Energy, TVA, Entergy, TECO, Tri-State Generation.

**Personas:** VP Engineering/Capital Projects, CIO/CDO/VP IT/Director Digital Transformation.

**7-touch sequence:** Give-give-give-ask (value-add -> content share -> social proof -> consultation offer -> new angle -> urgency -> ask for meeting).

**Events:** DistribuTECH, IEEE PES, EUCI, EEI (C-suite), APPA (municipals), NRECA (coops).

---

## 19. Outreach Tool

**`aecai_outreach.py`** — CLI for AI-powered sales outreach via Ollama.

```bash
python3 aecai_outreach.py                  # Interactive menu
python3 aecai_outreach.py list              # Show all leads
python3 aecai_outreach.py draft 0           # Draft LinkedIn DM for lead #0
python3 aecai_outreach.py batch linkedin    # Batch all LinkedIn drafts
python3 aecai_outreach.py batch email       # Batch all email drafts
```

3 message types: LinkedIn DM, Cold Email, Follow-up. Templates embed founder context (13 years exp, $1.85M proof point). Saves drafts to `data/drafts/`.

---

## 20. Marketing Agent

**Location:** `echology/marketing/` (gitignored from repo)

Automated content generation system. Detects shipping events (GitHub releases/tags), generates blog posts (EN + PT) and LinkedIn drafts using Claude CLI.

**Channels:** blog (EN), blog_pt (PT), linkedin
**Voice:** First-person as Kyle, engineer-to-engineer, practitioner-first positioning
**Style guide:** `marketing/voice_corpus/style_guide.md`
**Database:** SQLite (`marketing.db`) tracks events, content, actions

---

## 21. Current State (as of 2026-02-21)

| Metric | Value |
|--------|-------|
| Completed engineering tasks | 58 |
| Passing tests (AECai) | 577 |
| Passing tests (Decompose) | 63 |
| **Total passing tests** | **640** |
| Test failures | 0 |
| Test duration | ~29s |
| Simulation-aware systems | 17 |
| API endpoints | 29 |
| Route modules | 10 |
| Supported file formats | 16+ |
| Built-in plugins | 5 |
| Temporal workflows | 6 |
| Temporal activities | 18 |
| Activity modules | 8 |
| Qdrant collections | 3 |
| Test files | 35 |
| Coverage minimum | 70% |
| Engine files (Vanta) | 13 |
| Engine files (Aletheia) | 6 |
| Engine files (Daedalus) | 6 |
| Config parameters | 30 |
| Lines of code (total engine) | ~19,900 |
| Core dependencies | 13 |
| Python version | 3.11 |

**Entity status:** Delaware C-Corp formed. EIN obtained. Operating in SC. Insurance pending.

---

## 28. Repository Structure

### AECai (`/Users/kylevines/aecai` -> `github.com/echology-io/aecai`, private)
```
aecai/
  engine/vanta/          # 13 files, ~12,600 LOC
  engine/aletheia/       # 6 files, ~4,100 LOC
  engine/daedalus/       # 6 files, ~3,200 LOC
  routes/                # 10 route modules + deps + models
  temporal/              # 6 workflows, 18 activities, 8 activity modules
  tests/                 # 36 test files, 577 tests
  aecai_server.py        # FastAPI server
  config.py              # 31 env-overridable params
  pipeline_ops.py        # Shared processing functions
  Dockerfile + docker-compose.yml
  Makefile
  pyproject.toml (v3.1.0)
  .venv/ (Python 3.11.13)
```

### Echology (`/Users/kylevines/echology` -> `github.com/echology-io/decompose`)
```
echology/
  src/decompose/         # Decompose library source
  tests/                 # 63 tests
  docs/                  # GitHub Pages -> echology.io (MUST stay in git)
  marketing/             # Marketing agent (gitignored)
  ops/                   # SOPs, outreach tool, site (gitignored)
  TASKS.md               # Local task tracker -> syncs to Notion
  ECHOLOGY.md            # This document
  CHANGELOG.md
  pyproject.toml (v0.1.1)
  .venv/ (Python 3.11)
```

### RBS Demo (`/Users/kylevines/kylevines/rbs-demo` -> `github.com/echology-io/rbs-demo`, private)
```
rbs-demo/
  server.py              # ~1700 lines, FastAPI port 8600
  index.html             # Dashboard
  sample_data.json       # Pre-extracted test data
  data/STL PQC/          # Test documents
  .venv/ (Python 3.11)
```

### Personal Site (`/Users/kylevines/kylevines`)
- kylevines.com (GitHub Pages)
- Blog: `blog/why-i-build.html` and others

---

## 29. SOPs and Docs Inventory

| Document | Location | Status |
|----------|----------|--------|
| This document | `echology/ECHOLOGY.md` | Current |
| AECai Cheat Sheet | `echology/ops/sops/AECai_Cheat_Sheet.md` | Current (v3.2.0) |
| Outbound Sales SOP | `echology/ops/sops/AECai_Outbound_Sales_SOP.docx` | Current (v1.0) |
| Email Sequences | `echology/ops/sops/AECai_Email_Sequences.md` | Current (v1.0) |
| Assessment Template | `echology/ops/assessment_deliverable_template.md` | Current (v1.0) |
| Utility Outreach Strategy | `echology/ops/sops/AECai_Utility_Outreach_Strategy.docx` | Refresh market data |
| Utility Tracker | `echology/ops/sops/AECai_Utility_Outreach_Tracker.xlsx` | Working spreadsheet |
| Product Suite SOP | `echology/ops/sops/Echology_Product_Suite_SOP.md` | Current (v4.0) |
| Deployment Guide | `echology/ops/sops/Echology_Deployment_Guide.md` | Current (v4.0) |
| Architecture Doc | `echology/ops/ECHO_ARCH_001_Product_Suite_Architecture.md` | Current (v4.0) |
| Architecture Reference | `aecai/docs/architecture/aecai_architecture.txt` | Current (Gen 1.5) |
| Complete Reference | `aecai/docs/aecai_complete_reference.txt` | Current (Gen 1.5) |
| Gen 2.0 Roadmap | `echology/ops/gen2_roadmap.md` | Current (v1.0) |
| Technical Overview | `echology/ops/yc/AECai_Technical_Overview.md` | Current (v3.2.0) |
| YC Application | `echology/ops/yc/AECai_YC_Application_Spring2026_FINAL.docx` | Submitted Feb 9 |
| Task Tracker | `echology/TASKS.md` -> Notion | Current |
| Changelog | `echology/CHANGELOG.md` | Current |
| Blog: Why I Build | `kylevines/blog/why-i-build.html` | Current |

---

## 30. Interactive Roadmap

### Week 0: Launch Prep (current)

- [x] Platform built and tested (640 tests, 0 failures)
- [x] Sales strategy documented (cheat sheet, outbound SOP, utility strategy)
- [x] Pricing tiers defined ($800 / $5-15K / $100-250K)
- [x] ICP and buyer personas defined
- [x] Warm intro list mapped (30+ names)
- [x] Outreach tool built (aecai_outreach.py)
- [x] Marketing agent built (shipping event detection, blog/LinkedIn gen)
- [x] Narrative corrected and consistent across all docs
- [x] EIN obtained
- [x] Delaware C-Corp formed
- [x] Decompose on PyPI, MCP Registry, ClawHub
- [x] echology.io live (bilingual EN + PT)
- [x] kylevines.com live with blog
- [x] RBS demo built and functional
- [x] Notion task tracker synced (58 completed, 35 backlog, 18 research)
- [ ] SC foreign qualification filed
- [ ] Business insurance obtained (liability, cyber, E&O)
- [x] Discovery assessment deliverable template finalized
- [x] LinkedIn profile updated with consulting positioning
- [x] echology.io updated with consulting offer ($800 AECai assessment on contact + aecai pages)

### Week 1: Day 1 — Activate Outbound

- [ ] Send first 5 warm intros (personal messages, not templates)
- [ ] Begin LinkedIn engagement ritual (like/comment on 10 target prospects)
- [x] Draft first 3 LinkedIn posts (4 drafted in proposals/linkedin-posts.md)
- [ ] Publish first LinkedIn post
- [x] Set up lead tracking in Notion CRM (Clients DB: Source, Stage, First Contact, Notes fields + 3 leads imported)
- [ ] Review and update warm intro list — prioritize by relationship strength

### Week 2: Build Pipeline

- [ ] Send remaining warm intros (target: 20 total by end of week)
- [ ] Send first LinkedIn DMs to engaged prospects
- [x] Draft email Sequence A (connection -> opening -> follow-ups)
- [x] Draft email Sequence B (buying signal trigger)
- [x] Draft email Sequence C (retirement/knowledge loss trigger)
- [ ] Publish second LinkedIn post
- [ ] Schedule first discovery calls (target: 2-3 conversations)

### Weeks 3-4: First Assessments

- [ ] Conduct first discovery calls
- [ ] Book first paid assessment ($800)
- [ ] Begin assessment delivery (2-week turnaround)
- [ ] Start email Sequence C (retirement trigger)
- [ ] Publish weekly LinkedIn post
- [ ] Begin phone follow-ups on opened-but-no-reply emails
- [ ] File SC foreign qualification (if not done in Week 0)

### Days 31-60: Prove the Model

- [ ] Deliver first assessment(s)
- [ ] Collect first testimonial / case study data
- [ ] Book 3-4 additional assessments (target: 5-7 total)
- [ ] Move 1-2 assessment clients toward full engagement pipeline
- [ ] Refine assessment deliverable based on first delivery
- [ ] Identify product gaps from real engagement feedback
- [ ] Apply for business insurance (if not done)

### Days 61-90: First Revenue

- [ ] Close first full engagement ($15K-$75K)
- [ ] Publish first case study
- [ ] Reach 4-6 assessments/month run rate
- [ ] Build $50K-$100K pipeline
- [ ] Reach 2-3 active clients
- [ ] Evaluate: product features needed vs. backlog priorities
- [ ] Begin utility-specific outreach (if pipeline supports it)

### Quarter 2: Scale What Works

- [ ] Refine sales process based on 90 days of data
- [ ] Build `vanta export` and `vanta diff` (if client feedback demands it)
- [ ] Implement proposal generation (EchoDeck)
- [ ] Evaluate hiring needs
- [ ] Hit $100K+ cumulative revenue target
- [ ] Decide: platform self-serve vs. consulting-only for Phase 2

### Future (earned, not scheduled)

- [ ] Code signing and Homebrew distribution
- [ ] Cross-OS install support (Mac, Windows, Linux)
- [ ] Gen 2.0 Phase 1: PostgreSQL, JWT/RBAC, multi-tenancy
- [ ] Aletheia blockchain anchoring
- [ ] Public API and SDK
- [ ] Procore/ACC integration
- [ ] Mobile apps

---

## 31. All Tasks — Complete Inventory

### Completed (58)

| # | Task | Date |
|---|------|------|
| 1 | Release Decompose standalone library (v0.1.2 on PyPI, MCP Registry, ClawHub) | 2026-02 |
| 2 | Build RBS Policy QC demo (insurance three-tier extraction pipeline) | 2026-02 |
| 3 | Build Polymarket trading system (5 strategies, paper + live dashboards) | 2026-02 |
| 4 | Execute repo separation (aecai / echology) | 2026-02 |
| 5 | Write unified theory + positioning realignment | 2026-02 |
| 6 | Implement filter_for_llm() in Decompose library | 2026-02 |
| 7 | Add structural entity validators to Vanta core | 2026-02 |
| 8 | Implement deterministic-first document classification | 2026-02 |
| 9 | Add Decompose pre-filter to Vanta pipeline (Stage 1.5) | 2026-02 |
| 10 | Build Temporal workflow integration (6 workflows, 18 activities) | 2026-02 |
| 11 | Build FastAPI server (aecai_server.py, port 8443) | 2026-02 |
| 12 | Build kylevines.com personal site | 2026-02 |
| 13 | Build Aletheia verification engine | 2026-02 |
| 14 | Build Daedalus retrieval and report generation engine | 2026-02 |
| 15 | Setup SSH Access: Windows Surface to Mac Mini M4 Pro | 2025-09 |
| 16 | Migrate proven CLI system from Windows to macOS | 2025-09 |
| 17 | Benchmark performance improvements (Mac mini) | 2025-09 |
| 18 | Install and configure JetBrains suite | 2025-09 |
| 19 | Design and develop homepage with brand story | 2025-09 |
| 20 | Set up blog homepage with category filters | 2025-09 |
| 21 | Build VANTA CLI architecture | 2025-11 |
| 22 | Define input formats (PDF, DOCX, TXT, CSV, DWG, DXF, RVT, IFC) | 2025-09 |
| 23 | Task, deadline, person, and entity detection | 2025-09 |
| 24 | Smart chunking and data processing | 2025-09 |
| 25 | Implement vanta redact (PII/BII anonymization) | 2025-09 |
| 26 | Test with industry datasets | 2025-09 |
| 27 | Large-file stress tests | 2025-09 |
| 28 | Create benchmark suite for performance testing | 2025-09 |
| 29 | Documentation completeness audit | 2025-09 |
| 30 | Build dashboards: Exec KPIs, Product Ops, Sales, Legal, Finance | 2025-09 |
| 31 | Structure operations environment | 2025-09 |
| 32 | Develop investor pitch deck | 2025-09 |
| 33 | Define and document pipeline | 2026-02 |
| 34 | Core Framework Development (Vanta engine) | 2026-02 |
| 35 | EchoPipeline Module (vanta_pipeline.py) | 2026-02 |
| 36 | EchoSecure Module (vanta_security.py) | 2026-02 |
| 37 | EchoDeck Module (daedalus_report.py) | 2026-02 |
| 38 | EchoAgents Module (vanta_plugins.py) | 2026-02 |
| 39 | Testing and QA (577 AECai + 63 Echology tests) | 2026-02 |
| 40 | Create databases: Tasks, Projects, CRM, Content | 2026-02 |
| 41 | Integrate task management (Scrum/Kanban via Notion) | 2026-02 |
| 42 | Notion Command Center | 2026-02 |
| 43 | Operations Stack (Namecheap, ProtonMail, Notion, GitHub) | 2026-02 |
| 44 | Write Aletheia vision one-pager | 2026-02 |
| 45 | Social bios (LinkedIn, GitHub, echology.io) | 2026-02 |
| 46 | Add author bios (Kyle Vines on echology.io + kylevines.com) | 2026-02 |
| 47 | Build Lazy Reality Scheduler (LRS) | 2026-02 |
| 48 | Build Quantum-Discrete Network Protocol (QDNP) | 2026-02 |
| 49 | Build Hierarchical Reality Virtual Machine (HRVM) | 2026-02 |
| 50 | Implement Causal Consistency Networks (CCN) | 2026-02 |
| 51 | Build Memetic Algorithm Resource Evolution (MARE) | 2026-02 |
| 52 | CAD/BIM vector extraction | 2026-02 |
| 53 | DWT/DXF CLI pipeline utilities | 2026-02 |
| 54 | Docker images for enterprise deployment | 2026-02 |
| 55 | Package Vanta for pip (PyPI v3.1.0) | 2026-02 |
| 56 | Industry-specific agent bundles (5 plugins) | 2026-02 |
| 57 | Security whitepaper (local-first air-gap) | 2026-02 |
| 58 | Obtain EIN | 2026-02 |

### In Progress (1)

| Task | Notes |
|------|-------|
| Activate AECai consulting launch — outbound sales Day 1 | Warm intros first, then LinkedIn engagement, then email sequences. $800 assessment offer. |

### Backlog (35 items)

**Legal/Entity:**
- Open S-Corp (or C-Corp election)
- Entity formation completion
- SC foreign qualification (operating state update)
- 409A valuation preparation
- Business insurance (liability, cyber, E&O)
- Legal documentation
- Schema registry and contracts

**Marketing:**
- Content calendar
- VSL video sales letter
- YT: Why start now?
- Marketing strategy

**Business:**
- Business development strategy
- Business strategy
- Conduct buyer interviews (5-10 per target market)
- Start list-building with waitlist signup
- Define success criteria for beta users
- Define funding ask ($1M-$2.5M Seed)
- Design email sequences (cold, follow-up, nurture)

**Product:**
- Implement `vanta export` (JSON -> CSV/XLSX/Markdown)
- Implement `vanta diff` (compare doc revisions)
- Cross-OS install smoke tests
- Create install docs for Windows, Mac, Linux
- Professional proposal document generation (EchoDeck)
- Generate SOPs and slide decks from pipeline outputs
- Auto-attach certification reports in decks
- Redaction policy documentation
- Telemetry guardrails (opt-in vs opt-out)
- Create ECSIT Systemization Offer sheet

**Distribution:**
- Apple Developer enrollment and code-signing certificates
- Code signing and release trust implementation
- Package for Homebrew or other CLI channels

**Ops:**
- Uptime status page setup

### Research — Blockchain/Aletheia Anchoring (18 items, future)

- Define blockchain integration rationale
- Write "local-first + chain-anchored" principle
- Draft cross-industry compliance reviews (MiCA, SEC, OFAC)
- Create enterprise DAO governance templates
- Pick success metrics (verifiability, latency, fees, ops burden)
- Compare L2s for anchoring/payments
- Decide primary L2 for anchors/payments; backup chain
- Define testnet strategy
- Implement cross-chain temporal consensus prototype
- Choose DID method compatible with local use
- Issue/verify VCs locally; optionally anchor on-chain
- Design anchor contract: store (hash, timestamp, metadata)
- Add CLI: `aletheia certify --anchor`
- Implement cross-chain anchors
- Specify state-root hashing for Aletheia ledger snapshots
- Write verifier CLI: `aletheia verify --proof <bundle>`
- Define VCs for: dataset cert, reviewer identity, organization role
- Build DID integration for reviewer identity

---

## 32. Risk to Watch

- Drifting into abstraction without tangible deployed systems
- Becoming a research lab instead of shipping vertical systems with real metrics
- Letting tools overshadow the practitioner story in positioning
- Building product features speculatively before user/client feedback
- AI-generated narratives drifting from Kyle's actual words and experience
- Over-engineering Gen 2.0 features before consulting revenue validates direction

---

## 33. Notion Integration

**Tasks: Workflow DB:** `collection://2682973f-06dc-8190-aa33-000bef5503cd`
**DB URL:** `https://www.notion.so/2682973f06dc8115b832efbe10cf82ef`
**Board view:** `view://2682973f-06dc-8126-a90a-000c49de5eb4` (Kanban by Bucket)
**Full table view:** `view://2682973f-06dc-818c-b42d-000c36513f3b`

**Property mapping:**
- `Status` (select): New, In Progress, Completed, On Hold, Achieved, Cancelled
- `Bucket` (select with emojis): `.01 Inbox` through `.25 Archive`
- `Status 1` (status): Not started, In progress, Done
- To mark complete: Status=Completed, Bucket=`.24 Complete`, Status 1=Done

**Sync protocol:** Edit `TASKS.md` locally -> batch-sync via `notion-update-page` MCP tool. Notion is source of truth for interactive review.

---

## 34. Infrastructure Notes

**Hardware:** Mac Mini M4 Pro, 8-core, 16GB RAM, 512GB internal SSD
**Storage:** echo_dev (1TB external SSD), echo_backup (1.8TB external HDD)
**Training data:** `/Volumes/echo_dev/aecai_data/aecai_training/`
**Qdrant storage:** `/Volumes/echo_dev/aecai_data/qdrant_storage/`
**System Python:** 3.9.6 — always use .venv with Python 3.11

**Debugging notes:**
- Server needs ~10-15s to load all Vanta modules on startup
- Qdrant data on echo_dev flash drive — not running locally unless drive connected
- Time Machine local snapshots DISABLED (was eating disk space)
