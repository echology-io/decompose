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

## 8. AECai Platform

Local-first AI platform for Architecture, Engineering, and Construction (AEC) firms. Reads any document a firm produces or receives — specs, submittals, contracts, RFIs, inspection reports, drawings — turns it into structured, searchable, verified data. No cloud. No per-seat SaaS. Runs on the firm's own hardware.

**Value proposition:**
- Recovers $300K-$500K annually per firm (CAD rework reduction alone)
- Replaces 2 days of junior engineer manual spec review with 30-second AI processing
- Captures institutional knowledge when senior engineers retire
- Cross-references jurisdiction-adopted building code editions
- NERC CIP compliant — no cloud API exposure

### Three Engines

| Engine | Files | LOC | Purpose |
|--------|-------|-----|---------|
| **Vanta** | 13 | ~12,600 | Parse, classify, enrich, decompose, index documents |
| **Aletheia** | 6 | ~4,100 | Verify output quality, jurisdiction code cross-reference, tamper-evident certification |
| **Daedalus** | 6 | ~3,200 | Retrieve patterns, generate intelligence reports, produce CAD/BIM scripts |

### Architecture

```
                     +------------------+
                     |   FastAPI Server  |  port 8443
                     |  aecai_server.py  |  29 endpoints, 10 route modules
                     +--------+---------+
                              |
          +-------------------+-------------------+
          |                   |                   |
+---------v------+  +--------v--------+  +-------v--------+
|     VANTA      |  |    ALETHEIA     |  |    DAEDALUS    |
|  13 files      |  |   6 files       |  |   6 files      |
|  ~12,600 LOC   |  |  ~4,100 LOC     |  |  ~3,200 LOC    |
|                |  |                 |  |                |
| Parse/Classify |  | Validate/Audit  |  | Retrieve/Gen   |
| Enrich/Chunk   |  | Jurisdiction    |  | Reports/CAD    |
| Index/Embed    |  | Certification   |  | BIM Scripts    |
+----------------+  +-----------------+  +----------------+
          |                   |                   |
          +-------------------+-------------------+
                              |
                +-------------v--------------+
                |     Temporal Orchestration  |
                |  6 workflows, 18 activities |
                +----------------------------+
```

### Document Pipeline (6 stages, every document)

```
PARSE -> PRE-FILTER -> CLASSIFY -> ENRICH -> DECOMPOSE -> INDEX
```

| Stage | Module | What Happens |
|-------|--------|-------------|
| **Parse** | `vanta_core.py` -> `TextExtractor.extract(filepath)` | 16+ formats (PDF, DOCX, DXF, CSV, images via OCR). Returns raw_text, cleaned_text, metadata |
| **Pre-Filter** | `decompose` lib (optional) -> `decompose_text()` + `filter_for_llm()` | Structured excerpt of high-value units + authority/risk profiles + standards as confidence signals |
| **Classify** | `vanta_classify_v2.py` -> `UniversalClassifier.classify_document(text, filename, structured_excerpt, decompose_hints)` | Deterministic-first: filename + regex + Decompose signals scored; >0.8 skips AI. Falls through to Ollama llama3 when signals weak. Entity validators reject invalid entities |
| **Enrich** | `vanta_plugins.py` -> `PluginRegistry.execute(text, classification, envelope)` | 5 built-in plugins: StandardsCrossref, PII, Timeline, Financial, Contract |
| **Decompose** | `vanta_core.py` -> `chunk_markdown()` / `chunk_text()` | Header-aware MD chunks or character-based with overlap. Per-unit classification (authority, risk, domain) |
| **Index** | `vanta_embed.py` + `vanta_index.py` | Embed (nomic-embed-text 768d or MiniLM 384d) -> upsert to Qdrant |

**Entry point:** `VantaPipeline.process_file(filepath)` in `vanta_pipeline.py`

**Shared processing:** `pipeline_ops.py` wraps VantaPipeline for server + Temporal, handles OCR routing, output mapping, auto-persist.

**Three output formats:**
- **Standard** — `_map_v2_output()` -> frontend-friendly (standards, obligations, risks, timeline)
- **Rich** — `_map_v2_rich()` -> full envelope with semantic units
- **Training** — `_export_training_jsonl()` -> one JSONL record per semantic unit

**Processing benchmarks:**
- Small doc (10 pages): ~2-5s
- Medium doc (50 pages): ~10-15s
- Large doc (200+ pages): ~30-60s
- Torsion optimization: ~21% speedup on low-signal content

---

## 9. Vanta Engine — Module Details (13 files)

| File | Key Class | What It Does |
|------|-----------|-------------|
| `vanta_core.py` | `TextExtractor`, `OllamaClient`, `ENTITY_VALIDATORS` | Text extraction (16+ formats), chunking, standards/entity detection, entity validators, envelope creation |
| `vanta_classify_v2.py` | `UniversalClassifier` | Deterministic-first classification: filename + regex + Decompose signals scored (>0.8 skips AI). Entity validators. 62 AEC keywords, 60+ doc type signatures |
| `vanta_plugins.py` | `PluginRegistry` | 5 enrichment plugins (standards, PII, timeline, financial, contract). Circuit breaker (3-failure quarantine). Extensible |
| `vanta_ai.py` | `AIEnhancementEngine` | Confidence-gated AI: only calls LLM when rule-based confidence < 0.70. Three-channel parity (regex + structure + AI -> majority vote) |
| `vanta_embed.py` | `EmbeddingEngine` | Local embeddings: Ollama nomic-embed-text (768d) -> sentence-transformers all-MiniLM-L6-v2 (384d) -> none |
| `vanta_index.py` | `VantaIndexManager`, `QdrantClient` | Qdrant vector store: 3 collections (documents, geometry, jurisdictions). HTTP-only, zero pip deps |
| `vanta_batch.py` | `BatchController`, `BatchManifest` | Parallel batch processing (4+ workers), content-hash dedup, incremental/resume modes |
| `vanta_geometry.py` | `GeometryExtractor` | DXF geometry: layers, blocks, entities, AIA/NCS naming (D-DISC-COMPONENT) |
| `vanta_pipeline.py` | `VantaPipeline` | Orchestrates all 5 stages. SimulationAwareEngine integration |
| `vanta_security.py` | `SecurityManager` | Input validation, AES-256 encryption, PII protection, ITAR/HIPAA scanning, hash-chained audit. NIST/ISO/SOC2/GDPR/CCPA/HIPAA/ITAR |
| `vanta_torsion.py` | `TorsionEngine`, `TorsionField` | Systems 1-4: Lazy scheduling, spin-curvature metadata, vortex caching, chirality feedback. Reduces wasted compute 30-70% |
| `vanta_simulation.py` | `SimulationAwareEngine` | Systems 5, 6, 8, 13, 15 (local) + composes Aletheia/Daedalus suites. Cross-engine coordinator |
| `__init__.py` | — | sys.path setup enabling cross-engine imports |

---

## 10. Aletheia Engine — Module Details (6 files)

| File | Key Class | What It Does |
|------|-----------|-------------|
| `aletheia_schema.py` | `SchemaValidator` | `.validate(data)` -> quality score (0-100), field-level pass/fail, cross-field invariants. Safety-critical keywords get 5x penalty |
| `aletheia_jurisdiction.py` | `JurisdictionRegistry`, `CrossReferenceEngine` | AHJ code adoption lookup. `.crossref(standards, ahj, state)` -> adopted/superseded/not_found. 500+ code bodies seeded |
| `aletheia_ledger.py` | `AuditLedger` | SQLite hash-chained ledger. `.issue_certificate(source, level)` — gold/silver/bronze only. SHA-256 chain verification |
| `aletheia_cli.py` | — | CLI: verify, validate, crossref, registry CRUD, ledger stats. `run_full_verification()` |
| `aletheia_simulation.py` | `AletheiaSimulationSuite` | Systems 7, 10, 11, 12, 14, 16: Causal chains, error correction, anchors, Merkle tree, anomaly detection, counterfactual logging |
| `__init__.py` | — | Package init |

**Certification levels:**
- **Gold**: quality >= 0.95, 0 errors, 0 mismatches
- **Silver**: quality >= 0.80, 0 errors
- **Bronze**: quality >= 0.60, <= 2 errors
- **None**: below thresholds

---

## 11. Daedalus Engine — Module Details (6 files)

| File | Key Class | What It Does |
|------|-----------|-------------|
| `daedalus_retrieve.py` | `RetrievalEngine` | `.search(query)` -> returns **dict** (not list). Qdrant vector search with jurisdiction/discipline/risk filters. Keyword fallback |
| `daedalus_report.py` | `ReportBuilder` | `.from_retrieval(results, ahj, state, type)` -> briefing/precedent/risk/prediction reports. MD/HTML/JSON |
| `daedalus_civil3d.py` | `PatternToScript` | `.generate_from_report(report)` -> .scr (AutoCAD), .lsp (AutoLISP) scripts |
| `daedalus_revit.py` | `PatternToRevit`, `DynamoBuilder` | `.generate_from_report(report)` -> .txt (journal), .dyn (Dynamo), .json (IFC crosswalk) |
| `daedalus_simulation.py` | `DaedalusSimulationSuite` | Systems 9, 17: HolographicStore (erasure-resilient), TopologicalBraid (PII/client isolation) |
| `__init__.py` | — | Package init |

**Report types:** briefing (what to know before submitting), precedent (how we've done this before), risk (standards and compliance risks), prediction (what AHJ is likely to comment on).

---

## 12. 17 Simulation-Aware Systems (SimArch — Internal IP)

| # | System | Engine | Class | One-liner |
|---|--------|--------|-------|-----------|
| 1 | Lazy Reality Scheduler | Vanta (torsion) | `TorsionEngine` | Defer expensive ops on low-signal chunks |
| 2 | Spin-Curvature Field | Vanta (torsion) | `TorsionField` | Physics-inspired importance/context metadata |
| 3 | Vortex Caching | Vanta (torsion) | `TorsionEngine` | Hot-spot persistence for repeated standards |
| 4 | Chirality Feedback | Vanta (torsion) | `TorsionEngine` | Compress <-> Decompose bidirectional learning |
| 5 | Quantum Discrete Protocol | Vanta (sim) | `QuantumDiscreteProtocol` | Deterministic batched message passing with causal ordering |
| 6 | Hierarchical Reality VM | Vanta (sim) | `HierarchicalRealityVM` | Nested document contexts with upward risk propagation |
| 7 | Causal Consistency Network | Aletheia | `CausalConsistencyNetwork` | Explainable causal chains for every finding (E&O defense) |
| 8 | Memetic Evolution | Vanta (sim) | `MemeticEvolution` | Self-improving detection patterns via genetic optimization |
| 9 | Holographic Store | Daedalus | `HolographicStore` | k-of-n erasure-resilient semantic unit storage |
| 10 | Quantum Error Corrector | Aletheia | `QuantumErrorCorrector` | Multi-channel parity (regex + structure + AI -> majority vote) |
| 11 | Reality Anchor System | Aletheia | `RealityAnchorSystem` | Known-true anchors cascade confidence to findings |
| 12 | Temporal Merkle Tree | Aletheia | `TemporalMerkleTree` | Unit-level tamper detection via Merkle DAG |
| 13 | Consciousness Scheduler | Vanta (sim) | `ConsciousnessScheduler` | Attention-budget allocation (safety_critical gets 4x) |
| 14 | Simulation Escape Detector | Aletheia | `SimulationEscapeDetector` | Anomaly detection: impossible dates, contradictory standards |
| 15 | Irreducibility Detector | Vanta (sim) | `IrreducibilityDetector` | Flags content that must be preserved verbatim |
| 16 | Counterfactual Logger | Aletheia | `CounterfactualLogger` | Logs decisions + alternatives ("what if we classified differently?") |
| 17 | Topological Braid | Daedalus | `TopologicalBraid` | Structural data segregation (PII/client isolation) |

**Coordinator:** `SimulationAwareEngine` in `vanta_simulation.py` composes all via `AletheiaSimulationSuite` + `DaedalusSimulationSuite`.

**File layout:**
- Systems 1-4: `engine/vanta/vanta_torsion.py`
- Systems 5, 6, 8, 13, 15: `engine/vanta/vanta_simulation.py`
- Systems 7, 10, 11, 12, 14, 16: `engine/aletheia/aletheia_simulation.py`
- Systems 9, 17: `engine/daedalus/daedalus_simulation.py`

---

## 13. Server and API

**`aecai_server.py`** — FastAPI on port 8443, 29 endpoints across 10 route modules.

**Middleware stack:** CORS -> API key auth (constant-time comparison) -> Security headers (CSP/HSTS) -> Docs localhost-only -> JSON body size limit -> Request logging.

**Security:** Magic byte validation, extension whitelist (18 types), path traversal detection, null byte filtering, rate limiting per IP.

### Endpoints (29 total)

| Route Module | Endpoints | Auth | Key Operations |
|-------------|-----------|------|----------------|
| `routes/process.py` | POST `/api/demo/process`, `/api/process`, `/api/process/rich`, `/api/export/training` | Rate-limited (demo), Localhost (rest) | Document processing (3 output modes) |
| `routes/documents.py` | GET `/api/documents`, `/api/documents/{filename}` | Localhost | Browse processed document history |
| `routes/chat.py` | GET `/chat`, POST `/api/chat` | Localhost | RAG-powered chat via Qdrant + Ollama SSE |
| `routes/health.py` | GET `/api/health` | Optional | Service status (pipeline, Ollama, OCR, Temporal, Qdrant) |
| `routes/leads.py` | POST `/api/leads`, GET `/api/leads`, DELETE `/api/leads/{id}`, DELETE `/api/leads` | POST public, rest Localhost | Lead capture + management + cleanup (JSONL) |
| `routes/projects.py` | POST `/api/projects`, GET `/api/projects`, GET `/api/projects/{id}` | Localhost | Project CRUD (JSON file) |
| `routes/feedback.py` | POST `/api/feedback`, GET `/api/feedback` | Localhost | User corrections on processed docs |
| `routes/jurisdictions.py` | GET `/api/jurisdictions`, POST `/api/jurisdictions`, GET `/api/jurisdictions/{ahj}/{state}` | Localhost | Jurisdiction registry CRUD (Aletheia) |
| `routes/workflows.py` | POST `/api/retrain`, `/api/verify`, `/api/report`, `/api/outreach` | Localhost | Temporal workflow triggers (SSE streaming) |
| `routes/pages.py` | GET `/`, `/app`, `/process`, `/outreach` | `/` public, rest Localhost | Static HTML page serving |

**Shared modules:** `routes/deps.py` (require_localhost, rate_limit), `routes/models.py` (Pydantic request/response models).

### Site Pages

| Page | Path | Purpose |
|------|------|---------|
| `index.html` | `/` (public) | Landing page |
| `app.html` | `/app` | Main dashboard |
| `process.html` | `/process` | Document processing GUI |
| `chat.html` | `/chat` | RAG chat interface |
| `outreach.html` | `/outreach` | Lead outreach tool |

---

## 14. Temporal Orchestration

**6 Workflows, 18 Activities, Task Queue: `aecai`**

| Workflow | What It Does | Timeout |
|----------|-------------|---------|
| `DocumentPipelineWorkflow` | Single doc through Vanta (standard/rich/training modes) | 10 min |
| `VerificationWorkflow` | Aletheia: validate -> crossref -> certify | 5 min |
| `IntelligenceReportWorkflow` | Daedalus: search -> report -> scripts | 15 min |
| `BatchProcessWorkflow` | Fan-out parallel multi-file processing | 60 min |
| `RetrainWorkflow` | Ingest -> convert JSONL -> LoRA fine-tune | 30/10/60 min |
| `BatchOutreachWorkflow` | Generate LinkedIn/email drafts per lead | 2 min/lead |

**Activity modules** (8 total): pipeline, aletheia, daedalus, batch, outreach, train, ingest, convert.

**Fallback:** When Temporal unavailable, server runs same code inline (no durable execution guarantees).

---

## 15. Training Pipeline

```
docs/sops/ -> ingest -> data/training/*.jsonl -> convert_training.py -> data/aecai_training/
     -> train_mlx.py (LoRA on llama3-8B-4bit, 600 iters, ~30 min on M4 Pro)
     -> ollama create aecai
```

Three training tasks per semantic unit:
- **Task A**: Classification + metadata extraction
- **Task B**: Risk & authority assessment
- **Task C**: Summary & context (units >50 words only)

**Config:** Base model mlx-community/Meta-Llama-3-8B-Instruct-4bit, batch size 1, LoRA layers 8, LR 1e-5, split 80/10/10. Output: ~8.5GB GGUF.

---

## 16. Decompose Library

**What:** Deterministic text classifier — authority, risk, attention, entities, irreducibility.
**How:** Pure regex + heuristics, no LLM, no API keys.
**Package:** `decompose-mcp` on PyPI (v0.1.1).

**API:**
```python
from decompose import decompose_text, filter_for_llm

result = decompose_text(text, chunk_size=2000, compact=True)
filtered = filter_for_llm(result, max_tokens=4000)
```

**Authority levels:** mandatory, prohibitive, directive, conditional, permissive, informational
**Risk categories:** safety_critical, compliance, financial, contractual, security, advisory, informational
**Attention scores:** 0.0-10.0 composite of authority weight and risk multiplier

**filter_for_llm():** Pre-filters decompose output by authority/risk/type for LLM context windows. Proven in RBS demo (15 -> 22 fields extracted). Configurable by authority, risk, type, min_attention, max_tokens.

**CLI:** `python -m decompose --serve` (MCP stdio) or pipe via stdin
**MCP tools:** `decompose_text`, `decompose_url`
**Benchmarks:** 13.9ms avg per doc, 1,064 chars/ms, 63 tests passing
**Real-world test:** 10 Anthropic docs (20K chars) -> 43 units in 34ms

### Distribution Status

| Target | Status |
|--------|--------|
| PyPI | Published v0.1.1 (Trusted Publishers via GitHub Actions OIDC) |
| Official MCP Registry | Published via mcp-publisher |
| ClawHub / OpenClaw | Published v0.1.2 |
| Claude Code MCP | Configured at user level (`~/.claude.json`) |

### GitHub Actions (echology-io/decompose)
- CI: pytest on Python 3.10-3.13 + ruff lint
- Benchmark: runs on push, posts stats
- Deploy Pages: builds docs/ to GitHub Pages
- Release Drafter: auto-drafts releases
- Publish: triggered on release publish, uses PyPI Trusted Publishers

---

## 17. RBS Policy QC Demo

Insurance policy QC automation built as a consulting demo. Upload Quote + Policy + Application + TAM for one insured, engine extracts fields from each, cross-references, flags discrepancies.

**Server:** `server.py` (~1700 lines, FastAPI port 8600)
**Repo:** `github.com/echology-io/rbs-demo` (private)
**Dashboard:** http://localhost:8600
**Site page:** https://echology.io/rbs (noindex, direct URL only)

### Three-Tier Extraction Pipeline

```
Document -> is native text? --yes--> pdfplumber -> regex -> tables -> done
                            |no
                            +----> OCR (Tesseract 200dpi) -> regex
                                 -> Decompose filter -> Ollama llama3 text AI
                                 -> LLaVA vision (page images -> JSON)
```

- **Tier 1 (Regex):** Always runs. 15 property/GL/auto patterns, 10 auto-specific, 8 premium patterns.
- **Tier 2 (Decompose + Ollama):** Triggers when `len(fields) < 10` AND Ollama available. Decompose filters OCR text, Ollama extracts missing fields, validators reject invalid values.
- **Tier 3 (LLaVA Vision):** Triggers when `len(still_missing) >= 5` AND is_scanned=True. PDF -> page images -> LLaVA per page -> JSON. 90s timeout per call.

**Test results:** ICA Properties (scanned): 22/24 fields, ~42s. PSC Construction (native): 23 fields, all regex.

**Key pattern proved:** Decompose as LLM pre-filter improved extraction from 15 -> 22 fields. This pattern was back-ported into AECai's Vanta pipeline as Stage 1.5.

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

## 22. Configuration

**`config.py`** — 30 params, all env-overridable (`AECAI_` prefix).

| Category | Key Defaults |
|----------|-------------|
| AI | Ollama localhost:11434, model llama3, embed nomic-embed-text, threshold 0.70 |
| Chunking | 2000 chars, 200 overlap |
| Qdrant | localhost:6333 |
| Server | 127.0.0.1:8443, 50 MB upload, 10s rate limit, 1024 KB JSON body |
| Temporal | localhost:7233, UI 8233, namespace default, queue aecai |
| Aletheia | ~/.echology/aletheia/jurisdictions.json, ledger.db |
| Security | API key (empty = disabled), audit dir |
| Data | 90-day lead retention |
| Logging | INFO level, 10 MB rotation, 5 backups |

---

## 23. Data Layout

```
data/
  outputs/               # Per-doc JSON (_standard.json, _rich.json, _training.jsonl)
  training/              # Training JSONL per document
  aecai_training/        # Converted chat-format training data + adapters + GGUF
  drafts/                # Outreach drafts
  leads.jsonl            # Lead storage (UUID, IP, arbitrary fields)
  feedback.jsonl         # User corrections (document_id, field, original, corrected)
  projects.json          # Project registry (name, ahj, state, description)
  pipeline_outputs.jsonl # Aggregated processing results
```

All files use `fcntl` advisory locking to prevent corruption from concurrent requests.

---

## 24. Deployment

### Target Hardware
Mac Mini M4 Pro (8-core, 16GB RAM), 512GB internal SSD, 1TB external SSD (projects + Qdrant), 4TB external HDD (backups).

### Docker Compose — 5 services

| Service | Port | Resources |
|---------|------|-----------|
| Qdrant v1.13.2 | 6333 | 2 CPU / 2 GB |
| Temporal v1.26.2 | 7233 | 1 CPU / 1 GB |
| Temporal UI v2.31.2 | 8233 | 0.5 CPU / 256 MB |
| AECai Server (Python 3.11-slim) | 8443 | 2 CPU / 4 GB |
| AECai Worker (same image) | — | 2 CPU / 4 GB |

Ollama on host (GPU-accelerated), containers reach via `host.docker.internal:11434`. Non-root container user `aecai`. Health checks on all services.

### Service Start Order (local dev)
1. Docker -> Qdrant container (auto-restart)
2. Ollama (`ollama serve` or brew service)
3. Temporal dev server (`temporal server start-dev --db-filename temporal_dev.db`)
4. AECai worker (`python -m temporal.worker`)
5. AECai server (`python aecai_server.py`)

### Local Server Ports (all projects)
- AECai: port 8443
- Polymarket: port 8500
- RBS Demo: port 8600
- Temporal UI: port 8233

### Ollama Models
- `llama3` (4.7GB) — general text AI
- `llava` (4.7GB) — vision model for RBS
- `aecai` (8.5GB) — LoRA fine-tuned for AEC domain
- `nomic-embed-text` (274MB) — embeddings

---

## 25. Key API Call Patterns (Gotchas)

```python
# Vanta
VantaPipeline.process_file(filepath)                          # Returns full dict, not staged
UniversalClassifier.classify_document(text, filename)          # NOT .classify()
UniversalClassifier.classify_document(text, filename,
    structured_excerpt=None, decompose_hints=None)            # Extended signature with Decompose
PluginRegistry.execute(text, classification, envelope)         # No .load(), use .discover()

# Aletheia
SchemaValidator.validate(data)                                 # Returns quality score 0-100
CrossReferenceEngine.check_document(standards, ahj, state)     # Returns adopted/superseded/not_found
AuditLedger.issue_certificate(source, level, quality_score)    # Only gold/silver/bronze

# Daedalus
RetrievalEngine.search(query)                                  # Returns dict, not list
ReportBuilder.from_retrieval(results, ahj, state, type)       # NOT .build() or .generate()
PatternToScript.generate_from_report(report)                   # Same for PatternToRevit

# Decompose
from decompose import decompose_text, filter_for_llm
decompose_text(text, chunk_size=2000, compact=True)           # Core function
filter_for_llm(result, max_tokens=4000)                       # Pre-filter for LLM input
```

---

## 26. Dev Commands

```bash
# AECai
source .venv/bin/activate
python aecai_server.py                                         # Start server (8443)
python -m temporal.worker                                       # Start Temporal worker
temporal server start-dev --db-filename temporal_dev.db         # Dev Temporal
make check                                                      # Lint + test + audit
make test                                                       # Tests only (30s timeout)
make test-cov                                                   # Tests + coverage report
make lint                                                       # Ruff lint + format check
make format                                                     # Auto-format
make smoke-up && make smoke-test && make smoke-down             # Integration tests
python engine/vanta/vanta_simulation.py inventory               # System inventory

# Outreach
python3 aecai_outreach.py                                       # Interactive outreach

# Training
python3 convert_training.py                                     # Convert training data
python3 train_mlx.py                                            # Run LoRA fine-tuning

# Decompose
cd ~/echology && .venv/bin/python -m pytest tests/ -v           # Run Decompose tests
python -m decompose --serve                                     # Start MCP server
```

---

## 27. Gen 2.0 Roadmap (18 months, 6 phases — future, earned)

| Phase | Months | Focus | Key Deliverables |
|-------|--------|-------|-----------------|
| 1 | 1-3 | Foundation | PostgreSQL migration, JWT/RBAC auth, multi-tenancy, API versioning, OpenTelemetry |
| 2 | 3-6 | Real-Time | WebSocket live status, webhooks (HMAC-signed), SSE streaming, Redis rate limiting |
| 3 | 4-8 | Intelligence | Hybrid RAG (vectors + BM25), cross-encoder re-ranking, ML A/B testing, proactive alerts, active learning |
| 4 | 6-10 | Document Mgmt | Versioning with semantic diff, annotations/comments, approval workflows, jurisdiction comparison |
| 5 | 8-14 | Ecosystem | Civil3D/Revit COM agents, public API + SDKs, Procore/ACC integration, Slack/Teams bots, plugin marketplace (WASM) |
| 6 | 12-18 | Enterprise | Envelope encryption (HSM/KMS), SAML SSO + SCIM, SOC 2 Type II cert, HA deployment, iOS/Android apps, edge agent |

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
- [ ] Set up lead tracking in Notion CRM
- [ ] Review and update warm intro list — prioritize by relationship strength

### Week 2: Build Pipeline

- [ ] Send remaining warm intros (target: 20 total by end of week)
- [ ] Send first LinkedIn DMs to engaged prospects
- [ ] Draft email Sequence A (connection -> opening -> follow-ups)
- [ ] Draft email Sequence B (buying signal trigger)
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
