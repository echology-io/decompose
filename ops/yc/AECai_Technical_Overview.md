# AECai — Technical Overview

**Version 3.2.0 | February 2026 | Echology, Inc.**

---

## What AECai Is

AECai is a local-first document intelligence platform built for Architecture, Engineering, and Construction (AEC) firms. It reads any document a firm produces or receives — specs, submittals, contracts, RFIs, inspection reports, drawings — and turns it into structured, searchable, verified data. No cloud. No per-seat SaaS. Runs on the firm's own hardware.

The system has three engines:

- **Vanta** — Reads, classifies, and decomposes documents into semantic units. Includes simulation-aware pipeline orchestration: deterministic message passing, nested document contexts, self-improving detection patterns, attention-budget scheduling, and irreducibility detection for content that must be preserved verbatim.
- **Aletheia** — Verifies output quality and checks standards against local building code adoptions. Includes simulation-aware verification: causal consistency graphs for audit defense, multi-channel error correction, anchor-relative confidence scoring, Merkle-tree tamper detection, anomaly detection, and counterfactual decision logging.
- **Daedalus** — Retrieves patterns from the firm's processed archive and generates CAD/BIM scripts. Includes simulation-aware data governance: holographic redundancy encoding for erasure-resilient storage, and topological braid-based data segregation for structural PII/client isolation.

Together, they form a pipeline: a document goes in, and structured intelligence comes out — classified, enriched, verified, and indexed for retrieval.

---

## Why It Exists

AEC firms drown in documents. A mid-size engineering firm handles thousands of specs, submittals, change orders, and inspection reports per project. Partners and PMs spend hours cross-referencing standards, checking code adoptions, and hunting through old projects for precedent.

The industry has no good tooling for this. Existing solutions are cloud-only, require manual tagging, or only handle one document type. AECai handles all of them — automatically, locally, with no manual setup.

The business moat is the jurisdiction data. Every city and county in the US adopts building codes differently — different editions, different amendments, different effective dates. AECai maintains a structured registry of these adoptions. When a firm processes a document, the system doesn't just detect that it references "IBC 2021" — it checks whether the Authority Having Jurisdiction (AHJ) has actually adopted that edition.

---

## How It Works

### The Pipeline

Every document flows through five stages:

```
PARSE → CLASSIFY → ENRICH → DECOMPOSE → INDEX
```

**Stage 1: Parse.** TextExtractor reads the file. It handles 15+ formats — PDF, DOCX, DXF (CAD drawings), Markdown, CSV, HTML, RTF, images (via OCR with Tesseract), and more. Output: raw text, cleaned text, page-level splits, file metadata.

**Stage 2: Classify.** UniversalClassifier determines what the document is. It uses a local LLM (Ollama/Llama 3) as the primary classifier, with regex-based fallback when the LLM is unavailable. It detects document type (specification, contract, pay application, inspection report, etc.), content domains (engineering, legal, financial, safety), entities (standards codes, parties, locations, dates), risk indicators (deadlines, financial implications, safety-critical content, compliance risk), and authority level (mandatory, recommended, permissive). The classifier also recommends which enrichment plugins to run.

**Stage 3: Enrich.** A plugin registry executes domain-specific enrichment based on the classifier's recommendations. Five built-in plugins ship today:

| Plugin | What It Does |
|--------|-------------|
| Standards Crossref | Detects standard references (ASTM, ACI, AISC, NFPA, etc.) and checks jurisdiction adoption |
| PII Detection | Finds SSNs, phone numbers, emails, credit cards, DOBs, passport numbers |
| Timeline | Extracts dates and temporal events from the document |
| Financial Analysis | Extracts dollar amounts, percentages, financial terms |
| Contract Analysis | Identifies parties, obligations, and key terms in contracts |

Plugins are priority-ordered and extensible — firms can write their own.

**Stage 4: Decompose.** The document is chunked into semantic units. For Markdown files, chunking is header-aware (respects `#`/`##`/`###` hierarchy). For everything else, it uses character-based chunking with overlap. Each unit gets its own per-unit classification — authority level, content type, risk relevance, domain tags. This is where the document stops being a blob of text and becomes structured data.

**Stage 5: Index.** Each semantic unit is embedded (768-dim vectors via Ollama's nomic-embed-text, or 384-dim via sentence-transformers as fallback) and stored in Qdrant. This makes the firm's entire processed archive searchable by meaning, not just keywords.

### The Output

Every processed document produces a JSON envelope:

```json
{
  "_pipeline": { "version": "2.0.0", "stage": "complete", "engine": "vanta" },
  "_provenance": [{ "stage": "parse", "action": "extract", "timestamp": "..." }, ...],
  "metadata": { "filename": "...", "pages": 12, "word_count": 8500, "format": "pdf" },
  "classification": {
    "document_type": "specification",
    "content_domains": ["engineering", "construction_admin"],
    "entities": { "standards_codes": ["IBC 2021", "ASTM C150-20"], ... },
    "risk_indicators": { "safety_critical": true, "compliance_risk": true }
  },
  "plugins": {
    "standards_crossref": { "standards_found": 14, "jurisdiction_check": { ... } },
    "pii_detection": { "pii_detected": false }
  },
  "semantic_units": [
    {
      "text": "Steel framing shall comply with AISC 360-22...",
      "classification": { "authority_level": "mandatory", "content_type": "requirement" }
    }
  ],
  "summary": { "total_units": 47, "authority_profile": { "mandatory": 23, ... } }
}
```

Three output variants are generated per document:
- **Standard** — Classification, entities, standards, risk flags (what the UI displays)
- **Rich** — Full semantic units with cross-references (what retrieval uses)
- **Training JSONL** — One record per semantic unit with labels (what fine-tuning uses)

When simulation-aware processing is enabled, the pipeline additionally runs 17 systems across the three engines — Vanta handles pipeline orchestration (deterministic message passing, nested document contexts, memetic pattern evolution, attention scheduling, irreducibility detection), Aletheia handles verification (causal graphs, error correction, anchor confidence, Merkle proofs, anomaly detection, counterfactual logging), and Daedalus handles data governance (holographic encoding, topological segregation). A unified `SimulationAwareEngine` coordinator in Vanta composes all three and produces an integrated simulation report alongside the standard output.

---

## Verification: Aletheia

After Vanta processes a document, Aletheia can verify the output.

**SchemaValidator** scores the pipeline output for completeness and correctness — checking that mandatory fields exist, cross-field invariants hold (e.g., safety-critical content must reference standards), and units aren't empty or contradictory. It produces a quality score (0-100) and a certification level (bronze/silver/gold).

**JurisdictionRegistry** maintains structured data about which building codes each AHJ has adopted. When a document references "IBC 2021," the registry checks whether Clark County, NV actually adopted the 2021 edition or is still on 2018. This is the data that doesn't exist anywhere else in structured form.

**AuditLedger** records every validation and certification event in a hash-chained, append-only SQLite ledger. Each entry includes a SHA-256 chain hash linking it to the previous entry and an HMAC-SHA256 signature. The chain can be independently verified for tampering — if any entry is modified, the chain breaks. This produces an auditable compliance trail.

**Simulation-aware verification** adds six subsystems that operate alongside the core validators:

- **CausalConsistencyNetwork** — Builds a directed acyclic graph of causal relationships. Every classification has an explainable chain: "This unit was flagged safety-critical BECAUSE it references ACI 318 Seismic AND contains 'shall' AND the discipline is structural." This serves E&O insurance defense and NIST AU-6 audit compliance.
- **QuantumErrorCorrector** — Runs multiple independent extraction channels (regex, structural, AI) on the same content. Where channels agree: high confidence. Where they disagree: flag for review, correct by majority vote.
- **RealityAnchorSystem** — Known-true elements (standard numbers, dates, named entities) serve as confidence anchors. Findings inherit confidence from their anchors. If an anchor is invalidated, all dependent findings cascade to "suspect."
- **TemporalMerkleTree** — Merkle DAG over pipeline outputs. Any single semantic unit can be verified without downloading the entire dataset. Enables granular tamper detection at the unit level.
- **SimulationEscapeDetector** — Anomaly detection for documents: impossible date sequences, contradictory standard versions, circular references.
- **CounterfactualLogger** — Logs classification decisions AND their alternatives. "We classified this as safety_critical. If we had classified it as advisory, these downstream consequences would change." Enables learning and audit defense.

---

## Retrieval and Script Generation: Daedalus

Once documents are indexed, Daedalus turns the firm's archive into actionable output.

**RetrievalEngine** searches the Qdrant vector index by semantic similarity. A PM can query "fire safety requirements for Type II-B construction" and get back relevant semantic units from every processed document in the firm's archive, ranked by relevance, filterable by jurisdiction, discipline, or risk level. When Qdrant is unavailable, it falls back to keyword search across output files.

**ReportBuilder** synthesizes retrieval results into structured intelligence reports — pre-submittal briefings, risk analyses, or precedent summaries. Reports include jurisdiction profiles, adopted code status, risk warnings, design precedents from the firm's history, and recommendations.

**PatternToScript** and **PatternToRevit** convert patterns from reports into executable CAD/BIM automation:
- Civil3D: `.scr` (AutoCAD scripts), `.lsp` (AutoLISP routines) for alignments, pipe networks, grading
- Revit: `.txt` (journal files), `.dyn` (Dynamo node graphs), `.json` (IFC crosswalk mappings) for walls, framing, MEP systems

This closes the loop: documents in, structured intelligence out, executable scripts back into the design tools the firm already uses.

**Simulation-aware data governance** adds two subsystems:

- **HolographicStore** — Erasure-resilient semantic unit storage. Each unit is encoded with boundary information from its neighbors, so any k-of-n units can reconstruct the document's meaning. If 30% of the vector index is lost or corrupted, the full meaning is still recoverable.
- **TopologicalBraid** — Data segregation encoded as topological strands. PII strands structurally cannot cross with public strands. Client A strands structurally cannot cross with Client B strands. This isn't policy enforcement — it's structural impossibility in the data model.

---

## Architecture

### Server

FastAPI application on port 8443. 29 API endpoints across 10 route modules.

**Public endpoints** (rate-limited): Document processing demo, lead capture.
**Localhost-only endpoints**: All admin operations — processing, projects, documents, chat, workflows, jurisdictions, feedback.
**Authenticated endpoints**: Health check returns infrastructure details only with valid Bearer token.

Security middleware stack: CORS, API key auth (constant-time comparison), CSP headers (config-driven ports), HSTS, request size limiting, path traversal protection with magic byte verification on uploads.

### Workflow Orchestration

Six Temporal workflows handle long-running or multi-step operations:

| Workflow | What It Does |
|----------|-------------|
| DocumentPipeline | Single document through Vanta (standard, rich, or training mode) |
| Verification | Schema validation, jurisdiction crossref, certificate issuance |
| IntelligenceReport | Retrieval, report synthesis, CAD/BIM script generation |
| BatchProcess | Parallel multi-file processing (fan-out) |
| Retrain | Ingest docs, convert training data, run fine-tuning |
| BatchOutreach | Generate outreach drafts for a batch of leads via LLM |

18 activities registered across 8 activity modules. Task queue: `aecai`. When Temporal is unavailable, the server falls back to inline processing — the same code runs, just without durable execution guarantees.

### Data Storage

All local. No cloud dependencies.

- **Qdrant** — Vector database for semantic search (3 collections: documents, geometry, jurisdictions)
- **SQLite** — Audit ledger (WAL mode, hash-chained entries)
- **JSON/JSONL files** — Leads, feedback, projects, processed outputs, training data
- **File system** — Document outputs in `data/outputs/`, training corpus in `data/training/`

### Deployment

Docker Compose orchestrates five services:

| Service | Image | Resources |
|---------|-------|-----------|
| Qdrant | qdrant/qdrant:v1.13.2 | 2 CPU / 2 GB |
| Temporal | temporalio/auto-setup:1.26.2 | 1 CPU / 1 GB |
| Temporal UI | temporalio/ui:2.31.2 | 0.5 CPU / 256 MB |
| AECai Server | Custom (Python 3.11-slim) | 2 CPU / 4 GB |
| AECai Worker | Same image, different entrypoint | 2 CPU / 4 GB |

Non-root container user (`aecai`), health checks on all services, resource limits enforced. SOC 2-aligned: no secrets in images, rotating log files, atomic file writes with locking.

The entire stack runs on a single machine. Tested on Apple Silicon (M-series). Ollama runs on the host for GPU-accelerated inference — the containers reach it via `host.docker.internal`.

### AI Integration

All AI is local via Ollama. No API keys, no cloud inference, no data leaving the machine.

- **Classification**: Llama 3 (configurable) for document type, entities, risk analysis
- **Embeddings**: nomic-embed-text (768-dim) via Ollama, sentence-transformers fallback (384-dim)
- **Chat**: RAG-powered — retrieves relevant context from Qdrant, augments system prompt, streams via SSE
- **Outreach drafts**: LLM-generated LinkedIn/email drafts from lead data
- **Report narratives**: Optional LLM synthesis for intelligence report summaries

The confidence-gated AI enhancement engine (AIEnhancementEngine) only invokes the LLM when rule-based classification confidence falls below a threshold (default 0.70). This keeps inference costs low while still using AI where it matters.

---

## Security

SecurityManager implements a full compliance layer:

- **Input validation**: Magic byte verification, extension whitelist, path traversal detection, null byte filtering
- **PII protection**: Detection and optional redaction of SSNs, phone numbers, emails, credit cards, DOBs, passport numbers, driver's license numbers
- **Sensitive content scanning**: Trade secrets, ITAR-controlled content, HIPAA PHI
- **Encryption**: AES-256 via Fernet (PBKDF2 key derivation) for sensitive outputs
- **Provenance**: HMAC-SHA256 signed, hash-chained audit entries
- **Data governance**: Classification levels (public/internal/confidential/restricted) with handling rules
- **Secure I/O**: Atomic writes, secure delete (overwrite passes), file permissions (0o600)

Compliance frameworks addressed: NIST 800-53, ISO 27001:2022, SOC 2 Type II, GDPR, CCPA/CPRA, HIPAA, ITAR/EAR, OWASP Top 10.

---

## Test Suite

554 tests across 36 test files. All pass. Coverage threshold: 70%.

| Category | Test Files | Tests |
|----------|-----------|-------|
| Vanta Engine | 10 | ~200 |
| Aletheia | 4 | ~50 |
| Daedalus | 4 | ~40 |
| Server/API | 4 | ~50 |
| Routes | 6 | ~60 |
| Infrastructure | 7 | ~150 |
| Workflows | 1 | ~10 |

CI pipeline (GitHub Actions): lint (ruff) + test with Qdrant/Temporal services + dependency audit (pip-audit). Three independent jobs, 15-minute timeout.

Makefile targets: `make check` runs lint + coverage + audit in one command. `make smoke` starts Docker services, runs integration tests, stops services.

---

## Configuration

31 parameters, all with sensible defaults, all overridable via environment variables (`AECAI_` prefix).

Key defaults:
- LLM: Ollama on localhost:11434, model llama3
- Embeddings: nomic-embed-text
- Chunk size: 2000 chars, 200 overlap
- Upload limit: 50 MB
- Rate limit: 10 seconds per IP
- Lead retention: 90 days
- Log rotation: 10 MB per file, 5 backups

---

## What's Real vs. What's Planned

**Shipping today (Gen 1):**
- Full 5-stage pipeline (parse, classify, enrich, decompose, index)
- 15+ file format support including OCR
- AI-first classification with regex fallback
- 5 built-in enrichment plugins
- Header-aware Markdown chunking
- Jurisdiction registry with adoption tracking
- Hash-chained audit ledger with certification
- Semantic search via Qdrant
- Intelligence report generation
- Civil3D and Revit script generation
- RAG-powered chat
- 6 Temporal workflows with inline fallback
- 17 simulation-aware systems distributed across all 3 engines
- Full security/compliance layer
- Docker Compose deployment
- 554 passing tests

**Not yet built:**
- Multi-tenant support (current: single-firm deployment)
- Paid jurisdiction data service (registry is populated manually today)
- Web-based jurisdiction data management UI
- Fine-tuning pipeline completion (infrastructure exists, training loop needs finishing)
- Production monitoring/alerting (logging exists, dashboards don't)
- Horizontal scaling (single-machine today, Temporal enables multi-worker but untested at scale)

---

## Numbers

| Metric | Value |
|--------|-------|
| Python version | 3.11 |
| Core dependencies | 13 |
| API endpoints | 29 |
| Supported file formats | 15+ |
| Built-in plugins | 5 |
| Temporal workflows | 6 |
| Temporal activities | 18 |
| Qdrant collections | 3 |
| Test count | 554 |
| Test files | 36 |
| Coverage minimum | 70% |
| Engine modules (Vanta) | 13 files, ~12,600 lines |
| Engine modules (Aletheia) | 6 files, ~4,100 lines |
| Engine modules (Daedalus) | 6 files, ~3,200 lines |
| Simulation-aware systems | 17 (across all 3 engines) |
| Config parameters | 31 |
| Lines of code (total engine) | ~19,900 |
