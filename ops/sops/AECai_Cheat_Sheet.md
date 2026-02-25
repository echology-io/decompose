# AECai Platform Cheat Sheet

**v3.2.0 | Echology, Inc. (Delaware C-Corp) | February 2026**

---

## Company & Founder

**Kyle Vines** — Solo technical founder/CEO. 13+ years geotechnical/civil engineering. Acquired and ran a geotech firm. Last role: LaBella Associates (ENR Top 200) — adopted AI tools, validated them across 200 engineers, tools stuck. Charleston, SC, three kids. 19,000+ lines of production code, solo. Mother is CTO and cybersecurity board member — security in DNA, not bolted on.

**Core thesis**: "I adopted AI inside an engineering firm and it worked. Now I'm packaging those lessons so other firms can do the same."

---

## What AECai Is

Local-first AI platform for Architecture, Engineering, and Construction (AEC) firms. Reads any document a firm produces or receives — specs, submittals, contracts, RFIs, inspection reports, drawings — turns it into structured, searchable, verified data. **No cloud. No per-seat SaaS. Runs on the firm's own hardware.**

**Three engines:**
- **Vanta** — Parse, classify, enrich, decompose, index documents
- **Aletheia** — Verify output quality, check jurisdiction code adoptions, issue tamper-evident certificates
- **Daedalus** — Retrieve patterns from the firm's archive, generate intelligence reports, produce CAD/BIM scripts

**Value proposition:**
- Recovers $300K-$500K annually per firm (CAD rework reduction alone)
- Replaces 2 days of junior engineer manual spec review with 30-second AI processing
- Captures institutional knowledge when senior engineers retire
- Ensures compliance by cross-referencing jurisdiction-adopted building code editions
- No cloud API exposure = NERC CIP compliant for utility clients

---

## Competitive Moat (5 layers)

1. **Air-gapped architecture** — Only local-first product. Competitors require cloud. Engineering firms with NDA-protected data won't accept cloud. Non-negotiable.
2. **Jurisdiction code registry** — Structured data on which AHJ adopted which code edition with amendments. Doesn't exist elsewhere in queryable form.
3. **Domain-specific AI** — Understands ASCE 7, ACI 318, OSHA 29 CFR 1926, inter-entity relationships. Not generic document AI.
4. **Consulting-first positioning** — $800 assessment removes procurement friction, proves value before software commitment.
5. **Founder domain expertise** — 13 years in engineering = instant credibility with buyers.

---

## Business Model

| Tier | Price | Cycle |
|------|-------|-------|
| Discovery Assessment | $800 (immediate booking) / $1,000 standard | 2 weeks delivery, credit card, no PO |
| SaaS Subscription | $5K-$15K/month per firm | Monthly |
| Enterprise | $100K-$250K annually | Multi-office firms |

Assessment fee credits 100% toward full engagement. Cost per client after onboarding: ~$0 (no cloud compute, no API fees). Gross margins >90%.

**TAM**: Top 500 ENR firms x $10K/month avg = $60M ARR from Tier 1 alone. Thousands more mid-market firms below that.

---

## Sales Strategy: Consulting First, Not SaaS

**Positioning**: "I'm an engineer-turned-consultant who happens to build AI tools" — NOT a vendor pitching software. Engineer-to-engineer, peer not vendor.

### Ideal Customer Profile

**Firmographics**: ENR Top 500, 50+ engineers, civil/structural/geotech/environmental, $50M+ revenue.

**Buyer personas** (in authority order):
1. VP of Engineering / Chief Engineer
2. Director of Operations
3. Principal / Associate Principal
4. CTO / Director of Innovation
5. Regional Director

**Buying signals** (pursue if 2+ present):
- Hiring "Document Control Manager" or "Knowledge Management"
- Senior engineer (20+ years) recently retired/departed
- Won large new contract ($50M+)
- "Digital transformation" or "AI adoption" in company news
- Failed audit or compliance issue
- Rapid headcount growth (10%+ past year)
- Multiple offices / geographic expansion
- Active on Procore, Bluebeam, ProjectWise

**Anti-targets**: Under 30 engineers, pure architecture, construction-only GCs, existing competitor relationships, IT Directors without engineering background.

### Outbound Sales Phases

**Phase 1 — Warm Intros** (highest priority, 3-5x conversion):
- 30+ mapped names (former colleagues, ASCE contacts, subs, vendors)
- 5-8 warm intros/day, Days 3-5

**Phase 2 — LinkedIn**:
- 3-day engagement ritual (like/comment before messaging)
- Day 5 opening: reference specific firm news, no pitch, ask for 15min call
- Follow-ups Days 4, 9, 16 with new angles, then break-up
- Content: 3x/week posts (the Dave Story, the Page 247 Story, vulnerability stories)

**Phase 3 — Email Sequences**:
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

**Why utilities**: Massive doc burden (single transmission project = 10,000+ pages), NERC CIP = air-gap non-negotiable, 40-50% workforce retirement-eligible in 5-10 years, billions in grid modernization budgets.

**Tier 1 targets**: Southern Company, Duke Energy, NextEra, Dominion, Xcel Energy, TVA, Entergy, TECO, Tri-State Generation.

**Personas**: VP Engineering/Capital Projects, CIO/CDO/VP IT/Director Digital Transformation.

**7-touch sequence**: Give-give-give-ask (value-add -> content share -> social proof -> consultation offer -> new angle -> urgency -> ask for meeting).

**Events**: DistribuTECH, IEEE PES, EUCI, EEI (C-suite), APPA (municipals), NRECA (coops).

---

## Architecture at a Glance

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

---

## The Pipeline (6 stages, every document)

```
PARSE -> PRE-FILTER -> CLASSIFY -> ENRICH -> DECOMPOSE -> INDEX
```

| Stage | Module | What Happens |
|-------|--------|-------------|
| **Parse** | `vanta_core.py` -> `TextExtractor.extract(filepath)` | 16+ formats (PDF, DOCX, DXF, CSV, images via OCR). Returns raw_text, cleaned_text, metadata |
| **Pre-Filter** | `decompose` lib (optional) -> `decompose_text()` + `filter_for_llm()` | Produces structured excerpt of high-value units + authority/risk profiles + standards as confidence signals |
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

## Engine Modules

### Vanta — Document Intelligence (13 files)

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

### Aletheia — Verification & Audit (6 files)

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

### Daedalus — Retrieval & Generation (6 files)

| File | Key Class | What It Does |
|------|-----------|-------------|
| `daedalus_retrieve.py` | `RetrievalEngine` | `.search(query)` -> returns **dict** (not list). Qdrant vector search with jurisdiction/discipline/risk filters. Keyword fallback |
| `daedalus_report.py` | `ReportBuilder` | `.from_retrieval(results, ahj, state, type)` -> briefing/precedent/risk/prediction reports. MD/HTML/JSON |
| `daedalus_civil3d.py` | `PatternToScript` | `.generate_from_report(report)` -> .scr (AutoCAD), .lsp (AutoLISP) scripts |
| `daedalus_revit.py` | `PatternToRevit`, `DynamoBuilder` | `.generate_from_report(report)` -> .txt (journal), .dyn (Dynamo), .json (IFC crosswalk) |
| `daedalus_simulation.py` | `DaedalusSimulationSuite` | Systems 9, 17: HolographicStore (erasure-resilient), TopologicalBraid (PII/client isolation) |
| `__init__.py` | — | Package init |

**Report types**: briefing (what to know before submitting), precedent (how we've done this before), risk (standards and compliance risks), prediction (what AHJ is likely to comment on).

---

## 17 Simulation-Aware Systems

| # | System | Engine | Class | One-liner |
|---|--------|--------|-------|-----------|
| 1 | Lazy Reality Scheduler | Vanta (torsion) | `TorsionEngine` | Defer expensive ops on low-signal chunks |
| 2 | Spin-Curvature Field | Vanta (torsion) | `TorsionField` | Physics-inspired importance/context metadata |
| 3 | Vortex Caching | Vanta (torsion) | `TorsionEngine` | Hot-spot persistence for repeated standards |
| 4 | Chirality Feedback | Vanta (torsion) | `TorsionEngine` | Compress <-> Decompose bidirectional learning |
| 5 | Quantum Discrete Protocol | Vanta (sim) | `QuantumDiscreteProtocol` | Deterministic batched message passing with causal ordering |
| 6 | Hierarchical Reality VM | Vanta (sim) | `HierarchicalRealityVM` | Nested document contexts with upward risk propagation |
| 7 | Causal Consistency Network | **Aletheia** | `CausalConsistencyNetwork` | Explainable causal chains for every finding (E&O defense) |
| 8 | Memetic Evolution | Vanta (sim) | `MemeticEvolution` | Self-improving detection patterns via genetic optimization |
| 9 | Holographic Store | **Daedalus** | `HolographicStore` | k-of-n erasure-resilient semantic unit storage |
| 10 | Quantum Error Corrector | **Aletheia** | `QuantumErrorCorrector` | Multi-channel parity (regex + structure + AI -> majority vote) |
| 11 | Reality Anchor System | **Aletheia** | `RealityAnchorSystem` | Known-true anchors cascade confidence to findings |
| 12 | Temporal Merkle Tree | **Aletheia** | `TemporalMerkleTree` | Unit-level tamper detection via Merkle DAG |
| 13 | Consciousness Scheduler | Vanta (sim) | `ConsciousnessScheduler` | Attention-budget allocation (safety_critical gets 4x) |
| 14 | Simulation Escape Detector | **Aletheia** | `SimulationEscapeDetector` | Anomaly detection: impossible dates, contradictory standards |
| 15 | Irreducibility Detector | Vanta (sim) | `IrreducibilityDetector` | Flags content that must be preserved verbatim |
| 16 | Counterfactual Logger | **Aletheia** | `CounterfactualLogger` | Logs decisions + alternatives ("what if we classified differently?") |
| 17 | Topological Braid | **Daedalus** | `TopologicalBraid` | Structural data segregation (PII/client isolation) |

**Coordinator:** `SimulationAwareEngine` in `vanta_simulation.py` composes all via `AletheiaSimulationSuite` + `DaedalusSimulationSuite`.

**File layout:**
- Systems 1-4: `engine/vanta/vanta_torsion.py`
- Systems 5, 6, 8, 13, 15: `engine/vanta/vanta_simulation.py`
- Systems 7, 10, 11, 12, 14, 16: `engine/aletheia/aletheia_simulation.py`
- Systems 9, 17: `engine/daedalus/daedalus_simulation.py`

---

## Server & API

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

---

## Temporal Orchestration

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

## Training Pipeline

```
docs/sops/ -> ingest -> data/training/*.jsonl -> convert_training.py -> data/aecai_training/
     -> train_mlx.py (LoRA on llama3-8B-4bit, 600 iters, ~30 min on M4 Pro)
     -> ollama create aecai
```

Three training tasks per semantic unit:
- **Task A**: Classification + metadata extraction
- **Task B**: Risk & authority assessment
- **Task C**: Summary & context (units >50 words only)

**Config**: Base model mlx-community/Meta-Llama-3-8B-Instruct-4bit, batch size 1, LoRA layers 8, LR 1e-5, split 80/10/10. Output: ~8.5GB GGUF.

---

## Outreach Tool

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

## Configuration

**`config.py`** — 31 params, all env-overridable (`AECAI_` prefix).

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

## Data Layout

```
data/
  outputs/           # Per-doc JSON (_standard.json, _rich.json, _training.jsonl)
  training/          # Training JSONL per document
  aecai_training/    # Converted chat-format training data + adapters + GGUF
  drafts/            # Outreach drafts
  leads.jsonl        # Lead storage (UUID, IP, arbitrary fields)
  feedback.jsonl     # User corrections (document_id, field, original, corrected)
  projects.json      # Project registry (name, ahj, state, description)
  pipeline_outputs.jsonl  # Aggregated processing results
```

All files use `fcntl` advisory locking to prevent corruption from concurrent requests.

---

## Deployment

### Target Hardware
Mac Mini M4 Pro (8-core, 16GB RAM), 512GB internal SSD, 1TB external SSD (projects + Qdrant), 4TB external HDD (backups).

### Docker Compose — 5 services

| Service | Port | Resources |
|---------|------|-----------|
| Qdrant v1.13.2 | 6333 | 2 CPU / 2 GB |
| Temporal v1.26.2 | 7233 | 1 CPU / 1 GB |
| Temporal UI v2.31.2 | 8233 | 0.5 CPU / 256 MB |
| AECai Server (Python 3.11-slim) | 8443 | 2 CPU / 4 GB |
| AECai Worker (same image) | - | 2 CPU / 4 GB |

Ollama on host (GPU-accelerated), containers reach via `host.docker.internal:11434`. Non-root container user `aecai`. Health checks on all services.

### Service Start Order (local dev)
1. Docker -> Qdrant container (auto-restart)
2. Ollama (`ollama serve` or brew service)
3. Temporal dev server (`temporal server start-dev --db-filename temporal_dev.db`)
4. AECai worker (`python -m temporal.worker`)
5. AECai server (`python aecai_server.py`)

---

## Site (HTML)

| Page | Path | Purpose |
|------|------|---------|
| `index.html` | `/` (public) | Landing page |
| `app.html` | `/app` | Main dashboard |
| `process.html` | `/process` | Document processing GUI |
| `chat.html` | `/chat` | RAG chat interface |
| `outreach.html` | `/outreach` | Lead outreach tool |

---

## Test Suite

**554 tests, 36 files, 70% coverage minimum**

| Category | Files | Focus |
|----------|-------|-------|
| Vanta engine | 10 | core, classify, plugins, AI, embed, index, batch, geometry, pipeline, security |
| Simulation | 3 | vanta_simulation, aletheia_simulation, daedalus_simulation |
| Torsion | 1 | Systems 1-4 |
| Aletheia | 2 | ledger, markdown ingestion |
| Daedalus | 3 | retrieve, report, general |
| Server/Routes | 10 | process, documents, chat, health, leads, projects, feedback, pages, upload validation, verify |
| Infrastructure | 5 | auth, config, integration, pipeline_ops, workflows |

**`make check`** = lint + test + audit. **CI:** GitHub Actions (3 jobs: lint, test w/ Qdrant+Temporal, pip-audit). 15-minute timeout.

---

## Key API Call Patterns (Gotchas)

```python
VantaPipeline.process_file(filepath)                          # Returns full dict, not staged
UniversalClassifier.classify_document(text, filename)          # NOT .classify()
PluginRegistry.execute(text, classification, envelope)         # No .load(), use .discover()
AuditLedger.issue_certificate(source, level, quality_score)    # Only gold/silver/bronze
RetrievalEngine.search(query)                                  # Returns dict, not list
ReportBuilder.from_retrieval(results, ahj, state, type)       # NOT .build() or .generate()
PatternToScript.generate_from_report(report)                   # Same for PatternToRevit
```

---

## Gen 2.0 Roadmap (18 months, 6 phases)

| Phase | Months | Focus | Key Deliverables |
|-------|--------|-------|-----------------|
| 1 | 1-3 | Foundation | PostgreSQL migration, JWT/RBAC auth, multi-tenancy, API versioning, OpenTelemetry |
| 2 | 3-6 | Real-Time | WebSocket live status, webhooks (HMAC-signed), SSE streaming, Redis rate limiting |
| 3 | 4-8 | Intelligence | Hybrid RAG (vectors + BM25), cross-encoder re-ranking, ML A/B testing, proactive alerts, active learning |
| 4 | 6-10 | Document Mgmt | Versioning with semantic diff, annotations/comments, approval workflows, jurisdiction comparison |
| 5 | 8-14 | Ecosystem | Civil3D/Revit COM agents, public API + SDKs, Procore/ACC integration, Slack/Teams bots, plugin marketplace (WASM) |
| 6 | 12-18 | Enterprise | Envelope encryption (HSM/KMS), SAML SSO + SCIM, SOC 2 Type II cert, HA deployment, iOS/Android apps, edge agent |

---

## Dev Commands

```bash
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
python3 aecai_outreach.py                                       # Interactive outreach
python3 convert_training.py                                     # Convert training data
python3 train_mlx.py                                            # Run LoRA fine-tuning
```

---

## SOPs & Docs Inventory

| Document | Location | Status |
|----------|----------|--------|
| Technical Overview | `docs/yc/AECai_Technical_Overview.md` | **Current** (v3.2.0) |
| YC Application | `docs/yc/AECai_YC_Application_Spring2026_FINAL.docx` | Current (submitted Feb 9) |
| Outbound Sales SOP | `docs/sops/AECai_Outbound_Sales_SOP.docx` | **Current** (v1.0, Feb 2026) |
| Utility Outreach Strategy | `docs/sops/AECai_Utility_Outreach_Strategy.docx` | **Refresh market data** (Feb 2025) |
| Utility Tracker | `docs/sops/AECai_Utility_Outreach_Tracker.xlsx` | Working spreadsheet |
| Product Suite SOP | `docs/sops/Echology_Product_Suite_SOP.md` | **Current** (v4.0, replaces stale .docx) |
| Deployment Guide | `docs/sops/Echology_Deployment_Guide.md` | **Current** (v4.0, merges 2 stale .docx) |
| Architecture Doc | `docs/architecture/ECHO_ARCH_001_Product_Suite_Architecture.md` | **Current** (v4.0, replaces stale .docx) |
| Architecture Reference | `docs/architecture/aecai_architecture.txt` | **Current** (Gen 1.5, updated Feb 14) |
| Complete Reference | `docs/aecai_complete_reference.txt` | **Current** (Gen 1.5, updated Feb 14) |
| Gen 2.0 Roadmap | `docs/gen2_roadmap.md` | **Current** (v1.0, baseline fixed) |
| Sim Aware Notes | `docs/sim aware.rtf` | **Superseded** (split is complete) |

---

## Verified Numbers (Feb 14, 2026)

| Metric | Value |
|--------|-------|
| Python version | 3.11 |
| Core dependencies | 13 |
| API endpoints | 29 |
| Route modules | 10 |
| Supported file formats | 15+ |
| Built-in plugins | 5 |
| Temporal workflows | 6 |
| Temporal activities | 18 |
| Activity modules | 8 |
| Qdrant collections | 3 |
| Test count | 554 |
| Test files | 36 |
| Coverage minimum | 70% |
| Engine files (Vanta) | 13 |
| Engine files (Aletheia) | 6 |
| Engine files (Daedalus) | 6 |
| Simulation-aware systems | 17 (across all 3 engines) |
| Config parameters | 31 |
| Lines of code (total engine) | ~19,900 |
