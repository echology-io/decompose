# Echology Product Suite — Standard Operating Procedures

**Version 4.0 | February 2026**

**Author:** Echology, Inc.

| Product | Role | Modules | Lines |
|---------|------|---------|-------|
| **VANTA** | Document Intelligence Engine | 13 files | 11,887 |
| **ALETHEIA** | Verification and Compliance | 6 files | 4,121 |
| **DAEDALUS** | Retrieval and Automation | 6 files | 3,198 |

**Total: ~99 Python files | ~31,414 lines | 100% local / air-gapped**

CONFIDENTIAL -- Echology, Inc. | Delaware C-Corp

---

## Table of Contents

1. [Product Overview](#1-product-overview)
2. [Pipeline Operations (Vanta)](#2-pipeline-operations-vanta)
3. [Verification Operations (Aletheia)](#3-verification-operations-aletheia)
4. [Retrieval and Generation Operations (Daedalus)](#4-retrieval-and-generation-operations-daedalus)
5. [Simulation-Aware Processing](#5-simulation-aware-processing)
6. [Workflow Orchestration (Temporal)](#6-workflow-orchestration-temporal)
7. [Security Operations](#7-security-operations)
8. [Training Operations](#8-training-operations)
9. [Operational Procedures](#9-operational-procedures)
10. [Module Inventory](#10-module-inventory)
11. [Configuration Reference](#11-configuration-reference)
12. [Error Handling and Graceful Degradation](#12-error-handling-and-graceful-degradation)
13. [Troubleshooting](#13-troubleshooting)
14. [Document Control](#14-document-control)

---

## 1. Product Overview

### 1.1 Purpose and Scope

AECai is a local-first AI platform purpose-built for Architecture, Engineering, and Construction (AEC) firms. It processes any document type encountered in professional practice, verifies outputs against jurisdiction codes and quality standards, and converts institutional knowledge into actionable design intelligence and executable scripts.

The platform comprises three engines:

- **Vanta** -- Document intelligence. Extracts, classifies, enriches, decomposes, and indexes documents across 16+ file formats using AI-first universal classification.
- **Aletheia** -- Verification and compliance. Validates pipeline outputs against data contracts, cross-references standards against jurisdiction code adoptions, and maintains a tamper-evident audit ledger for certification.
- **Daedalus** -- Retrieval and automation. Queries the indexed knowledge base to surface patterns, generate intelligence reports, and produce executable design scripts for Civil3D and Revit.

### 1.2 Local-First Architecture

AECai runs entirely on-premises. Zero cloud dependencies. Zero data leaves the network. All AI inference (LLM classification, embeddings, chat) executes locally via Ollama. All vector storage is local via Qdrant. All audit records are local via SQLite. The system is designed for air-gapped deployment in regulated environments.

### 1.3 Target Audience

- Engineers and project managers uploading and processing documents
- System administrators deploying and maintaining the platform
- Developers extending the plugin architecture or integrating via API
- Compliance officers reviewing audit trails and certification records

### 1.4 Data Flow

```
Documents --> VANTA (Parse -> Classify -> Enrich -> Decompose -> Index)
                |
                v
          ALETHEIA (Validate -> Crossref -> Certify)
                |
                v
          DAEDALUS (Retrieve -> Synthesize -> Generate)
```

### 1.5 Deployment Summary

| Attribute | Vanta | Aletheia | Daedalus |
|-----------|-------|----------|----------|
| Modules | 13 | 6 | 6 |
| Lines of Code | 11,887 | 4,121 | 3,198 |
| Python Version | 3.10+ | 3.10+ | 3.10+ |
| External Services | Ollama, Qdrant | SQLite (built-in) | Qdrant, Ollama (optional) |
| Storage | JSON + Qdrant + SQLite | SQLite + JSON | Qdrant (read) |
| Air-Gap Ready | Yes | Yes | Yes |

---

## 2. Pipeline Operations (Vanta)

Vanta (Vertically Aligned Native Technology Architecture) is the document processing engine. All documents enter the system through Vanta's 5-stage pipeline.

**Entry point:** `VantaPipeline.process_file(filepath)` in `vanta_pipeline.py`

**Shared processing:** `pipeline_ops.py` wraps VantaPipeline for use by both the FastAPI server and Temporal workers.

### 2.1 The 6-Stage Pipeline

```
PARSE --> PRE-FILTER --> CLASSIFY --> ENRICH --> DECOMPOSE --> INDEX
```

> **Stage 1.5: Pre-Filter** (optional) — When Decompose library is installed, runs `decompose_text()` + `filter_for_llm()` to produce a structured excerpt of high-value units. Provides authority/risk profiles and standards as deterministic confidence signals for the classifier.

#### Stage 1 -- PARSE

`TextExtractor` reads the file and produces raw text plus metadata (filename, size, pages, format). Supports 16+ formats:

| Format Category | Supported Types | Extraction Method |
|-----------------|----------------|-------------------|
| PDF | `.pdf` | PyMuPDF (with OCR fallback via Tesseract for scanned documents) |
| Office | `.docx` | python-docx |
| CAD | `.dxf` | `vanta_geometry.py` (AIA layer parsing, block analysis) |
| Images | `.png`, `.jpg`, `.jpeg`, `.tiff`, `.tif`, `.bmp`, `.gif` | OCR via pytesseract + Pillow |
| Plain Text | `.txt`, `.md`, `.csv`, `.xml`, `.html`, `.json`, `.rtf` | Direct text extraction |

#### Stage 2 -- CLASSIFY

`UniversalClassifier.classify_document(text, filename, structured_excerpt, decompose_hints)` uses a **deterministic-first** approach. It combines filename hints (60+ patterns), regex authority analysis, and Decompose signals (authority/risk profiles, standards count) into a confidence score. When confidence exceeds 0.8, classification completes without any AI call (`classification_method: deterministic_high_confidence`). Below that, it falls through to Ollama (llama3) with regex fallback.

- **Deterministic-first:** Filename + regex + Decompose signals scored; >0.8 skips AI entirely.
- **AI path:** Uses structured excerpt (pre-filtered text) when available for cleaner AI input.
- **Entity validators:** All extracted entities validated structurally — rejects invalid emails, SSNs, dates, drawing numbers, etc.
- **Regex fallback:** When Ollama is unavailable, produces complete classification from regex + filename heuristics. The `classification_method` field indicates `deterministic_high_confidence`, `ai_primary`, or `regex_fallback`.

#### Stage 3 -- ENRICH

`PluginRegistry` checks which loaded plugins match the classification's `suggested_plugins` and content indicators. Matching plugins execute in priority order.

Five built-in plugins run automatically when relevant content is detected:

| Plugin | Priority | Activates When | Output |
|--------|----------|----------------|--------|
| `pii_detection` | 10 | HR, legal, safety, insurance, medical content | PII type counts, redaction recommendation |
| `standards_crossref` | 20 | Formal references detected (any type) | Standards inventory, jurisdiction check readiness |
| `contract_analysis` | 30 | Contract/agreement types, legal domain + mandatory authority | Parties, contract sum, termination/indemnification clauses |
| `financial_analysis` | 35 | Financial implications or financial domain content | Monetary values, percentages, financial metrics |
| `timeline_construction` | 40 | Deadlines flagged, contract/report/schedule types | Chronological event list with context |

Plugin execution: `PluginRegistry.execute(text, classification, envelope)` -- note that `.discover()` (not `.load()`) is used to find plugins.

#### Stage 4 -- DECOMPOSE

Text is split into header-aware markdown chunks or character-based chunks (default 2,000 characters with 200-character overlap, configurable via `AECAI_CHUNK_SIZE` and `AECAI_CHUNK_OVERLAP`). Sentence-boundary detection prevents mid-sentence splits. Each chunk receives its own unit-level classification with authority level, risk relevance, actionable flag, and domain tags.

#### Stage 5 -- INDEX

`vanta_embed.py` generates local embeddings via Ollama (`nomic-embed-text`, 768 dimensions) or sentence-transformers (384 dimensions as fallback). `vanta_index.py` writes vectors and metadata to Qdrant across three collections: `documents`, `geometry`, and `jurisdictions`.

This stage is optional and requires Qdrant. The first four stages produce a complete JSON analysis independently.

### 2.2 Output Formats

Every processed document produces three output formats from a single pipeline run (no re-processing):

| Format | File Suffix | Description |
|--------|-------------|-------------|
| **Standard** | `_standard.json` | Frontend-optimized: classification, counts, sample extractions, knowledge profile, PII flag |
| **Rich** | `_rich.json` | Full `rich-v1` envelope: all semantic units, entity index with context windows, cross-references, evidence hierarchy, `requires_human_review` flags |
| **Training** | `_training.jsonl` | Chat-format JSONL: one record per semantic unit with document context, labels, structured extractions, cross-document linkage |

Output directory: `data/outputs/`

### 2.3 Pipeline Output Contract

Every processed document produces a standardized JSON envelope:

```json
{
  "_pipeline": { "version", "stage", "timestamp", "source_file", "engine", "elapsed_ms" },
  "_provenance": [ { "stage", "action", "timestamp", "details" } ],
  "_content_hash": "MD5 for deduplication",
  "metadata": { "filename", "size_bytes", "page_count", "word_count", "format" },
  "classification": { "document_type", "content_domains", "entities", "risk_indicators" },
  "plugins": { "plugin_name": { } },
  "semantic_units": [ { "text", "classification", "authority_analysis" } ],
  "summary": {
    "document_type", "content_domains", "total_units", "actionable_units",
    "authority_profile", "risk_profile", "risk_flags", "plugins_executed",
    "total_formal_references"
  }
}
```

### 2.4 Key Vanta API Calls

```python
from vanta_pipeline import VantaPipeline
from vanta_classify_v2 import UniversalClassifier
from vanta_plugins import PluginRegistry

# Process a file through the full 5-stage pipeline
pipeline = VantaPipeline(model="llama3", ollama_host="http://localhost:11434")
result = pipeline.process_file("/path/to/document.pdf")
# Returns full dict, not staged

# Classify a document directly
classifier = UniversalClassifier()
classification = classifier.classify_document(text, filename)
# Method is classify_document(), NOT .classify()

# Execute plugins against a classification
registry = PluginRegistry()
registry.discover()  # NOT .load() -- use .discover()
enrichments = registry.execute(text, classification, envelope)
```

---

## 3. Verification Operations (Aletheia)

Aletheia is the truth-grade data verification system. Named for the Greek concept of truth and disclosure, it validates Vanta outputs through a 3-step verification pipeline.

### 3.1 3-Step Verification Pipeline

#### Step 1 -- Schema Validation

`SchemaValidator.validate(vanta_output_dict)` validates Vanta JSON output against field contracts and produces a quality score from 0 to 100.

- Cross-field invariants are checked for internal consistency.
- Safety-critical fields carry a **5x penalty weight** for missing or invalid data.

**Certification levels:**

| Level | Quality Score | Error Threshold |
|-------|--------------|-----------------|
| **Gold** | >= 0.95 | 0 errors |
| **Silver** | >= 0.80 | 0 errors |
| **Bronze** | >= 0.60 | <= 2 errors |
| **None** | Below thresholds | -- |

#### Step 2 -- Jurisdiction Cross-Reference

`CrossReferenceEngine.check_document(vanta_output_dict)` cross-references detected standards against the `JurisdictionRegistry`, which maintains AHJ (Authority Having Jurisdiction) code adoption records.

Supported code bodies include: IBC, IRC, IPC, IMC, IFC, NEC, NFPA, ASCE, ACI, AISC, AWS, AASHTO, and others.

**Status outcomes:**

| Status | Meaning |
|--------|---------|
| `match` | Detected edition matches adopted edition |
| `edition_outdated` | Detected edition is older than adopted edition |
| `edition_newer` | Detected edition is newer than adopted edition |
| `edition_mismatch` | Edition detected but does not match |
| `no_edition_detected` | Standard found but no edition could be parsed |
| `no_registry` | Code body not in registry for the specified AHJ |

#### Step 3 -- Certification

`AuditLedger.issue_certificate(source, level, quality_score)` issues a certificate and records it in an append-only SQLite database.

- **Hash-chained entries:** Each entry is SHA-256 linked to the previous, creating a tamper-evident chain.
- **Chain verification:** `verify_chain()` validates the integrity of the entire ledger.
- **Accepted levels:** `gold`, `silver`, or `bronze` only. Any other value is rejected.

### 3.2 Key Aletheia API Calls

```python
from aletheia_schema import SchemaValidator
from aletheia_jurisdiction import CrossReferenceEngine
from aletheia_ledger import AuditLedger

# Validate a Vanta envelope
validator = SchemaValidator()
result = validator.validate(vanta_output_dict)

# Cross-reference against jurisdiction codes
engine = CrossReferenceEngine()
crossref = engine.check_document(vanta_output_dict)

# Issue a certificate
ledger = AuditLedger()
cert = ledger.issue_certificate(source="document.pdf", level="gold", quality_score=0.97)
# level must be "gold", "silver", or "bronze" -- no other values accepted
```

### 3.3 CLI Usage

```bash
# Seed the jurisdiction registry with default code bodies
python aletheia_cli.py registry seed

# Full verification pipeline
python aletheia_cli.py verify output.json --ahj "City of Henderson" --state NV --aec -v

# Schema validation only
python aletheia_cli.py validate output.json

# Cross-reference check
python aletheia_cli.py crossref output.json --ahj "City of Henderson" --state NV

# View ledger
python aletheia_cli.py ledger list

# Add a jurisdiction record
python aletheia_cli.py registry add --ahj "City of Henderson" --code IBC --edition 2021
```

### 3.4 Verification Disclaimer

All verification responses include the following advisory:

> ADVISORY ONLY. This certificate is generated by automated analysis and does not constitute professional engineering judgment, legal compliance verification, or official code review. All findings must be verified by a licensed professional before submission to any Authority Having Jurisdiction (AHJ).

---

## 4. Retrieval and Generation Operations (Daedalus)

Daedalus is the institutional memory and design intelligence system. Named for the master builder of Greek mythology, it queries the shared Qdrant vector store to surface relevant patterns, synthesize intelligence reports, and generate executable scripts for Civil3D and Revit.

### 4.1 Retrieval

`RetrievalEngine.search()` queries Qdrant for semantically similar content with optional structured filters for jurisdiction, discipline, and risk level.

```python
from daedalus_retrieve import RetrievalEngine

retriever = RetrievalEngine()
result = retriever.search(
    query="stormwater detention requirements",
    limit=10,
    min_score=0.3,
    ahj="City of Henderson",
    discipline="civil",
    risk_level="high",
)

# IMPORTANT: result is a dict, NOT a list
# Access patterns via result["results"]
patterns = result.get("results", [])
```

### 4.2 Report Generation

`ReportBuilder.from_retrieval(retrieval_result)` synthesizes retrieved patterns into structured intelligence reports.

| Report Type | Purpose |
|-------------|---------|
| **Briefing** | Pre-submittal briefing summarizing relevant precedents |
| **Precedent** | Design precedent report surfacing similar past project patterns |
| **Risk** | Risk assessment evaluating factors from historical data |
| **Prediction** | Predictive analysis based on pattern trends |

Output formats: Markdown, HTML, JSON.

### 4.3 Script Generation -- Civil3D

`PatternToScript.generate_from_report(report)` produces executable AutoCAD scripts:

| Output | Format | Description |
|--------|--------|-------------|
| AutoCAD Script | `.scr` | Command-line script for alignments, pipe networks, grading |
| AutoLISP | `.lsp` | Programmable routines with AIA/NCS layer name compliance |

### 4.4 Script Generation -- Revit

`PatternToRevit.generate_from_report(report)` produces Revit automation outputs:

| Output | Format | Description |
|--------|--------|-------------|
| Journal | `.journal` | Revit journal file for walls, framing, MEP |
| Dynamo Workspace | `.dyn` | Visual programming workspace definition |
| IFC Crosswalk | `.json` | Maps 17 IFC entity types to Revit categories |

---

## 5. Simulation-Aware Processing

AECai incorporates 17 simulation-aware processing systems distributed across three pillars. The `SimulationAwareEngine` in `vanta_simulation.py` coordinates all systems by composing `AletheiaSimulationSuite` and `DaedalusSimulationSuite`.

### 5.1 Three-Pillar Distribution

#### Vanta Torsion Systems (Systems 1--4)

Located in `vanta_torsion.py`. These operate at the document-processing level:

| System | Name | Function |
|--------|------|----------|
| 1 | Lazy Scheduling | Deferred computation scheduling for pipeline efficiency |
| 2 | Spin-Curvature | Document complexity and curvature analysis |
| 3 | Vortex Caching | Intelligent caching for repeated pattern access |
| 4 | Chirality Feedback | Asymmetric feedback loops for classification refinement |

#### Vanta Simulation Systems (Systems 5, 6, 8, 13, 15)

Composed by `SimulationAwareEngine` in `vanta_simulation.py`:

| System | Name |
|--------|------|
| 5 | QDNP (Quantum Document Navigation Protocol) |
| 6 | HRVM (Hierarchical Reality Verification Machine) |
| 8 | MemeticEvolution |
| 13 | ConsciousnessScheduler |
| 15 | IrreducibilityDetector |

#### Aletheia Simulation Systems (Systems 7, 10, 11, 12, 14, 16)

Located in `aletheia_simulation.py`:

| System | Name |
|--------|------|
| 7 | CCN (Consensus Compliance Network) |
| 10 | QEC (Quantum Error Correction) |
| 11 | RealityAnchorSystem |
| 12 | TemporalMerkleTree |
| 14 | SimulationEscapeDetector |
| 16 | CounterfactualLogger |

#### Daedalus Simulation Systems (Systems 9, 17)

Located in `daedalus_simulation.py`:

| System | Name |
|--------|------|
| 9 | HolographicStore |
| 17 | TopologicalBraid |

---

## 6. Workflow Orchestration (Temporal)

The system uses Temporal for durable workflow execution with automatic retry, step-level resumability, and progress streaming. All workflows and activities use the `aecai` task queue (configurable via `AECAI_TEMPORAL_TASK_QUEUE`).

### 6.1 Setup

```bash
# Start the Temporal dev server
temporal server start-dev --db-filename temporal_dev.db

# Start the AECai worker (requires .venv with Python 3.10+)
source .venv/bin/activate
python -m temporal.worker

# Web UI for monitoring
open http://localhost:8233
```

### 6.2 Workflows (6 Total)

| Workflow | Timeout | Trigger | Steps |
|----------|---------|---------|-------|
| `DocumentPipelineWorkflow` | 10 min | `/api/process`, `/api/process/rich`, `/api/export/training` | Process -> (optional) Rich -> (optional) Training -> Index |
| `VerificationWorkflow` | 5 min | `/api/verify` | Schema validate -> Jurisdiction crossref -> Certificate issuance |
| `IntelligenceReportWorkflow` | 15 min | `/api/report` | Retrieve patterns -> Generate report -> (optional) Generate scripts |
| `BatchProcessWorkflow` | 60 min | Internal | Discover files -> Process each -> Aggregate results |
| `RetrainWorkflow` | 30/10/60 min | `/api/retrain` | Ingest documents -> Convert training -> Train model |
| `BatchOutreachWorkflow` | 2 min/lead | `/api/outreach` | Load leads -> Draft for each lead |

### 6.3 Activities (18 Total)

| Group | Activities |
|-------|-----------|
| Document Pipeline | `process_document_standard`, `process_document_rich`, `process_document_training`, `index_document` |
| Batch Processing | `discover_files`, `process_single_file` |
| Aletheia Verification | `validate_schema`, `crossref_jurisdiction`, `issue_certificate`, `verify_ledger_chain` |
| Daedalus Intelligence | `retrieve_patterns`, `generate_report`, `generate_civil3d_script`, `generate_revit_script` |
| Retrain | `ingest_documents`, `convert_training`, `train_model` |
| Outreach | `draft_for_lead` |

### 6.4 Graceful Degradation

When Temporal is unavailable, all API endpoints fall back to inline (non-durable) processing. The server logs a warning and processes the request directly. Functionality is identical; durability and retry guarantees are lost.

```python
try:
    client = await get_temporal_client()
    result = await client.execute_workflow(
        WorkflowClass.run, args=[...], id=wf_id, task_queue="aecai"
    )
except Exception:
    log.warning("Temporal unavailable, falling back to inline processing")
    result = await process_inline(...)
```

---

## 7. Security Operations

### 7.1 Input Validation

Every uploaded file passes through multi-stage validation before processing:

| Layer | Implementation |
|-------|---------------|
| Filename Sanitization | Strips path components, null bytes, control characters; rejects path traversal patterns |
| Extension Whitelist | 18 allowed types: `.pdf`, `.docx`, `.doc`, `.txt`, `.md`, `.csv`, `.xml`, `.html`, `.json`, `.dxf`, `.rtf`, `.png`, `.jpg`, `.jpeg`, `.tiff`, `.tif`, `.bmp`, `.gif` |
| File Size Check | Configurable maximum (default 50 MB via `AECAI_MAX_UPLOAD_MB`) |
| Magic Byte Verification | First bytes compared against known signatures (`%PDF`, `PK\x03\x04`, `\x89PNG`, etc.) to confirm content matches claimed extension |
| Text Encoding Validation | UTF-8 or Latin-1 for text-based files; rejects binary content disguised as text |

### 7.2 PII Detection and Redaction

The `pii_detection` plugin detects and optionally redacts personally identifiable information:

| PII Type | Detection Method |
|----------|-----------------|
| Social Security Numbers | Pattern matching (XXX-XX-XXXX) |
| Phone Numbers | Multiple format patterns |
| Email Addresses | Standard email regex |
| Credit Card Numbers | Luhn-validated patterns |
| Dates of Birth | Date pattern with context analysis |
| Passport Numbers | Alphanumeric pattern with context |

### 7.3 Encryption

- **Algorithm:** AES-256 via Fernet symmetric encryption
- **Key Derivation:** PBKDF2 (Password-Based Key Derivation Function 2)
- **Application:** Optional at-rest encryption for sensitive pipeline outputs

### 7.4 Audit Trail

- **Signing:** HMAC-SHA256 signed entries for integrity verification
- **Chain:** SHA-256 hash-chained append-only ledger in SQLite
- **Verification:** `verify_chain()` validates the entire audit trail from genesis to latest entry

### 7.5 Compliance Mappings

`SecurityManager` in `vanta_security.py` implements compliance mappings for the following frameworks:

| Framework | Scope |
|-----------|-------|
| NIST 800-53 | Federal information security controls |
| ISO 27001 | International information security management |
| SOC 2 Type II | Service organization controls (security, availability, integrity) |
| GDPR | EU data protection regulation |
| CCPA | California consumer privacy act |
| HIPAA | Health information privacy and security |
| ITAR | International Traffic in Arms Regulations (export control) |

### 7.6 Server Security Architecture

| Layer | Implementation |
|-------|---------------|
| CORS | Locked to `localhost:8443` only (configurable, never wildcard) |
| Authentication | Bearer token via `AECAI_API_KEY` env var on all protected routes |
| Rate Limiting | Configurable per-IP rate limiting with automatic cleanup |
| Security Headers | X-Content-Type-Options, X-Frame-Options, XSS Protection, CSP, HSTS, Permissions-Policy |
| Temp Paths | `secrets.token_urlsafe()` crypto-random paths (not predictable timestamps) |
| API Docs | Swagger/ReDoc/OpenAPI disabled when `AECAI_API_KEY` is set |
| JSON Body | Configurable max JSON body size (default 1024 KB) |
| File Lifecycle | Uploaded files deleted immediately after processing (zero persistence) |

---

## 8. Training Operations

### 8.1 Training Data Ingestion

Documents processed through the Vanta pipeline are automatically converted to chat-format JSONL training records. Each semantic unit produces three training tasks per unit, covering classification, extraction, and analysis perspectives.

**Output files:**
- `data/outputs/{stem}_training.jsonl` -- pipeline output copy
- `data/training/{stem}_training.jsonl` -- training corpus copy

### 8.2 LoRA Fine-Tuning

Fine-tuning is performed on Apple Silicon hardware via MLX (Machine Learning Framework for Apple Silicon).

| Parameter | Value |
|-----------|-------|
| Base Model | Meta-Llama-3-8B-Instruct-4bit |
| Method | LoRA (Low-Rank Adaptation) |
| Framework | MLX |
| Iterations | 600 |
| Batch Size | 1 |
| Data Split | 80% train / 10% validation / 10% test |

### 8.3 Model Output

- **Format:** GGUF (approximately 8.5 GB)
- **Registration:** Registered with Ollama as `aecai-llama3`
- **Trigger:** One-click retraining via `POST /api/retrain` (SSE streaming progress) or via `RetrainWorkflow` in Temporal

### 8.4 Retrain Workflow Steps

1. **Ingest documents** -- Scan training corpus directory for available JSONL files
2. **Convert training** -- Transform documents into MLX-compatible training format with 80/10/10 split
3. **Train model** -- Execute LoRA fine-tuning (600 iterations), export to GGUF, register with Ollama

---

## 9. Operational Procedures

### 9.1 Daily Operations

| Task | Procedure | Verification |
|------|-----------|--------------|
| Monitor server logs | Review `server.log` for errors, warnings, and unusual patterns | No ERROR-level entries in the last 24 hours |
| Check Ollama model availability | Confirm `llama3` and `nomic-embed-text` models are loaded and responsive | `ollama list` shows both models |

### 9.2 Weekly Operations

| Task | Procedure | Verification |
|------|-----------|--------------|
| Verify audit ledger integrity | Run `verify_chain()` on the Aletheia audit ledger | Chain verification returns `intact: true` |
| Check Qdrant collection health | Query Qdrant for collection status and point counts | All three collections (`documents`, `geometry`, `jurisdictions`) are accessible |

### 9.3 Monthly Operations

| Task | Procedure | Verification |
|------|-----------|--------------|
| Review PII detection logs | Audit PII detection plugin output for false positives/negatives | Detection rates are within expected ranges |
| Update jurisdiction registry | Add new AHJ records, update code edition adoptions | `python aletheia_cli.py registry list` reflects current adoptions |
| Run security audit | Execute `pip-audit` against installed packages | No known vulnerabilities in production dependencies |

### 9.4 As-Needed Operations

| Task | Procedure |
|------|-----------|
| Process document batches | Upload via `POST /api/process` (multi-file) or use `BatchProcessWorkflow` |
| Generate intelligence reports | Submit query via `POST /api/report` with desired report type and filters |
| Retrain model | Trigger via `POST /api/retrain`; monitor SSE stream for progress |
| Add jurisdiction records | Use `python aletheia_cli.py registry add --ahj ... --code ... --edition ...` |
| Verify processed documents | Submit envelope to `POST /api/verify` with AHJ and state parameters |

---

## 10. Module Inventory

### 10.1 Summary

| Component | Files | Lines of Code |
|-----------|-------|---------------|
| Root (server, config, pipeline_ops) | 6 | 2,784 |
| Routes | 13 | 1,401 |
| Vanta (engine) | 13 | 11,887 |
| Aletheia (engine) | 6 | 4,121 |
| Daedalus (engine) | 6 | 3,198 |
| Temporal (worker, client, workflows, activities) | 19 | 1,461 |
| Tests | 36 | 6,562 |
| **Total** | **~99** | **~31,414** |

### 10.2 Test Coverage

- 36 test files covering all three engines, server routes, and Temporal workflows
- 554 tests total
- 6,562 lines of test code

### 10.3 Vanta Module Registry

| Module | Stage | Function |
|--------|-------|----------|
| `vanta_core.py` | SHARED | JSON envelope contracts, text extraction, entity extraction, semantic chunking, provenance chain |
| `vanta_classify_v2.py` | CLASSIFY | AI-first universal classification via Ollama, regex fallback, 3-channel parity voting |
| `vanta_plugins.py` | ENRICH | Plugin framework: registry, discovery, execution. 5 built-in plugins |
| `vanta_pipeline.py` | ORCHESTRATE | 5-stage pipeline orchestration with provenance tracking |
| `vanta_batch.py` | ORCHESTRATE | Parallel batch processing, content-hash dedup, incremental/resume |
| `vanta_index.py` | INDEX | Qdrant vector indexing across 3 collections, REST client |
| `vanta_embed.py` | INDEX | Local embeddings via Ollama nomic-embed-text (768d) or sentence-transformers (384d) |
| `vanta_ai.py` | ENHANCE | AI enrichment with confidence gating and fallback |
| `vanta_geometry.py` | PARSE | DXF geometry extraction, AIA layer parsing, block analysis |
| `vanta_torsion.py` | SIMULATE | Systems 1--4: lazy scheduling, spin-curvature, vortex caching, chirality feedback |
| `vanta_simulation.py` | SIMULATE | SimulationAwareEngine composing all 17 systems |
| `vanta_security.py` | SECURITY | Multi-framework compliance mappings |

### 10.4 Aletheia Module Registry

| Module | Stage | Function |
|--------|-------|----------|
| `aletheia_schema.py` | VALIDATE | Schema validation, field contracts, quality scoring 0--100, certification levels |
| `aletheia_jurisdiction.py` | CROSSREF | AHJ code adoption registry, standard reference parsing, cross-reference engine |
| `aletheia_ledger.py` | CERTIFY | SHA-256 hash-chained audit trail in SQLite, certificate issuance/revocation |
| `aletheia_cli.py` | ORCHESTRATE | Unified CLI: verify, validate, crossref, registry, ledger commands |
| `aletheia_simulation.py` | SIMULATE | Systems 7, 10, 11, 12, 14, 16 |

### 10.5 Daedalus Module Registry

| Module | Stage | Function |
|--------|-------|----------|
| `daedalus_retrieve.py` | RETRIEVE | Qdrant pattern search, semantic + structured filters |
| `daedalus_report.py` | SYNTHESIZE | Intelligence briefings, precedent reports, risk assessments, prediction reports |
| `daedalus_civil3d.py` | GENERATE | AutoCAD scripts (.scr), AutoLISP (.lsp), AIA layer compliance |
| `daedalus_revit.py` | GENERATE | Revit journals, Dynamo workspaces (.dyn), IFC crosswalk (.json, 17 entity types) |
| `daedalus_simulation.py` | SIMULATE | Systems 9, 17 |

---

## 11. Configuration Reference

All configuration lives in `config.py` via the `_Config` class. Every value has a sensible default for local development and can be overridden with environment variables using the `AECAI_` prefix.

**Usage:** `from config import cfg`

| Variable | Default | Description |
|----------|---------|-------------|
| **LLM** | | |
| `AECAI_OLLAMA_HOST` | `http://localhost:11434` | Ollama API endpoint |
| `AECAI_OLLAMA_MODEL` | `llama3` | Ollama model for AI classification and chat |
| **Embeddings** | | |
| `AECAI_EMBED_MODEL` | `nomic-embed-text` | Embedding model name |
| **Chunking** | | |
| `AECAI_CHUNK_SIZE` | `2000` | Semantic chunk size in characters |
| `AECAI_CHUNK_OVERLAP` | `200` | Overlap between chunks |
| **AI Enhancement** | | |
| `AECAI_AI_THRESHOLD` | `0.70` | Confidence threshold for AI enrichment |
| **Qdrant** | | |
| `AECAI_QDRANT_HOST` | `localhost` | Qdrant hostname |
| `AECAI_QDRANT_PORT` | `6333` | Qdrant port |
| **Server** | | |
| `AECAI_HOST` | `127.0.0.1` | Server bind address |
| `AECAI_PORT` | `8443` | Server port |
| `AECAI_MAX_UPLOAD_MB` | `50` | Maximum upload file size in MB |
| `AECAI_RATE_LIMIT_SECONDS` | `10` | Minimum seconds between requests per IP |
| `AECAI_MAX_JSON_BODY_KB` | `1024` | Maximum JSON body size in KB |
| `AECAI_CORS_ORIGINS` | `http://localhost:8443,http://127.0.0.1:8443` | CORS allowed origins |
| **Logging** | | |
| `AECAI_LOG_LEVEL` | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `AECAI_LOG_ROTATION_MB` | `10` | Log file rotation size in MB |
| `AECAI_LOG_BACKUP_COUNT` | `5` | Number of rotated log files to keep |
| **Workers** | | |
| `AECAI_WORKERS` | `1` | Uvicorn worker count |
| **Aletheia** | | |
| `AECAI_ALETHEIA_REGISTRY` | `~/.echology/aletheia/jurisdictions.json` | Jurisdiction registry path |
| `AECAI_ALETHEIA_LEDGER` | `~/.echology/aletheia/ledger.db` | Audit ledger path |
| `AECAI_DEFAULT_AHJ` | (empty) | Default Authority Having Jurisdiction |
| `AECAI_DEFAULT_STATE` | (empty) | Default state for jurisdiction lookups |
| **Security** | | |
| `AECAI_API_KEY` | (empty) | Bearer token; empty disables auth (local dev only) |
| `AECAI_SECURITY_AUDIT_DIR` | (empty) | Security audit log directory |
| **Data Retention** | | |
| `AECAI_LEAD_RETENTION_DAYS` | `90` | Days before leads auto-expire |
| **Temporal** | | |
| `AECAI_TEMPORAL_HOST` | `localhost:7233` | Temporal server address |
| `AECAI_TEMPORAL_NAMESPACE` | `default` | Temporal namespace |
| `AECAI_TEMPORAL_TASK_QUEUE` | `aecai` | Temporal task queue name |
| `AECAI_TEMPORAL_UI_PORT` | `8233` | Temporal Web UI port |
| **Paths** | | |
| `AECAI_BASE_DIR` | (project root) | Base directory for all data |

---

## 12. Error Handling and Graceful Degradation

The system is designed to degrade gracefully when external services are unavailable.

### 12.1 Ollama Unavailable

| Subsystem | Behavior |
|-----------|----------|
| Classification | Falls back from AI-primary to regex-based authority analysis + filename hints (60+ patterns). `classification_method` reads `regex_fallback`. |
| Embeddings | Falls back from Ollama `nomic-embed-text` (768d) to sentence-transformers (384d). |
| Chat | Returns an error message indicating Ollama is unreachable. |
| Reports | AI narrative is skipped; report is generated from structured data only. |

### 12.2 Qdrant Unavailable

| Subsystem | Behavior |
|-----------|----------|
| Indexing (Stage 5) | Skipped entirely. First four stages produce a complete JSON analysis. No error raised. |
| Retrieval | `RetrievalEngine.search()` returns an error dict (not an exception). Callers must check for `"error"` key. |
| Chat RAG | RAG retrieval is silently skipped; chat operates without document context. |

### 12.3 Temporal Unavailable

All API endpoints fall back to inline processing (non-durable). Functionality is identical; durability and retry guarantees are lost.

### 12.4 OCR Unavailable

- Scanned PDFs (no embedded text) return a `SCANNED_DOCUMENT` classification with zero counts.
- Image uploads return an `IMAGE` classification with zero counts.
- Documents with embedded text are unaffected.

### 12.5 Pipeline Load Failure

- If the Vanta pipeline fails to import, the server starts but processing endpoints return `RuntimeError: Vanta Pipeline not loaded`.
- The health endpoint reports `pipeline: false`.
- The server needs approximately 10--15 seconds to load all Vanta modules on startup.

---

## 13. Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|------------|
| AI classification shows `regex_fallback` | Ollama not running or model not pulled | `ollama serve && ollama pull llama3` |
| Upload rejected: content does not match extension | File extension does not match magic bytes | Ensure file is not corrupted or renamed with wrong extension |
| 401 Unauthorized | Missing or invalid API key | Set `AECAI_API_KEY` env var; include `Authorization: Bearer <key>` header |
| 429 Too Many Requests | Rate limit exceeded | Wait configured seconds or increase `AECAI_RATE_LIMIT_SECONDS` |
| No plugins activated | Document type not matching any plugin tags | Check classification output; plugins activate on domain/risk signals |
| Qdrant connection refused | Docker not running or wrong port | `docker run -d -p 6333:6333 qdrant/qdrant` |
| Schema validation returns 0 units | Input is not a Vanta JSON output | Process through Vanta pipeline first |
| Jurisdiction cross-ref: `no_registry` | Code body not in registry for AHJ | `python aletheia_cli.py registry add --ahj ... --code ... --edition ...` |
| Ledger chain integrity BROKEN | Ledger database modified externally | Restore from backup; entries are append-only |
| Server startup takes 10--15 seconds | Normal: loading all Vanta modules | Wait for startup banner to appear |
| `RuntimeError: Vanta Pipeline not loaded` | Pipeline import failed (missing dependencies) | Check `pip install` for all required packages; check server startup logs |
| Temporal workflow fails immediately | Worker not running or wrong task queue | `python -m temporal.worker` in activated venv |
| Chat returns Ollama unreachable | Ollama not running | `ollama serve` |
| OCR returns empty text | Tesseract not installed or image quality too low | `brew install tesseract`; check image resolution |
| `ImportError: temporalio` | System Python (3.9) used instead of venv | `source .venv/bin/activate` (requires Python 3.10+) |
| RetrievalEngine returns error dict | Qdrant not running | Check for `"error"` key in result before accessing `"results"` |

---

## 14. Document Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 2026 | Initial release: Vanta v1.3 (10 modules, 9,617 lines) |
| 1.3 | Feb 2026 | Updated deployment tiers, air-gap procedures, troubleshooting |
| 2.0 | Feb 2026 | Full trilogy: Added Aletheia (4 modules, 2,819 lines) and Daedalus (4 modules, 2,662 lines). Total: 18 modules, 15,098 lines |
| 3.0 | Feb 2026 | Architecture rebuild: AI-driven universal classifier replacing hardcoded keywords. Plugin framework with 5 built-in plugins. Secure FastAPI GUI. Total: 21 modules, 19,199 lines |
| 3.2 | Feb 2026 | Full codebase update: 25 modules totaling 19,206 lines. Simulation modules added. Server upgraded to 29 endpoints across 10 route modules. Temporal integration (6 workflows, 18 activities). Three processing modes. RAG-augmented chat. 31 config params |
| 4.0 | Feb 2026 | Comprehensive SOP rewrite. Expanded to ~99 files, ~31,414 lines. Added training operations (LoRA fine-tuning on Apple Silicon via MLX). Added operational procedures (daily/weekly/monthly checklists). Added full module inventory with line counts. Restructured security operations with PII, encryption, and compliance detail. Added simulation-aware processing section covering all 17 systems. Updated all API references and troubleshooting guidance |

---

*End of Document*
