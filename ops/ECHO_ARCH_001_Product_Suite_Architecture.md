# ECHO-ARCH-001: AECai Product Suite Architecture

| Field              | Value            |
|--------------------|------------------|
| **Version**        | 4.0              |
| **Date**           | February 2026    |
| **Author**         | Echology, Inc.   |
| **Classification** | Internal         |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Engine: Vanta -- Document Intelligence](#3-engine-vanta--document-intelligence)
4. [Engine: Aletheia -- Verification & Compliance](#4-engine-aletheia--verification--compliance)
5. [Engine: Daedalus -- Retrieval & Automation](#5-engine-daedalus--retrieval--automation)
6. [Simulation-Aware Systems](#6-simulation-aware-systems)
7. [API Architecture](#7-api-architecture)
8. [Workflow Architecture (Temporal)](#8-workflow-architecture-temporal)
9. [Data Architecture](#9-data-architecture)
10. [Security Architecture](#10-security-architecture)
11. [Deployment Architecture](#11-deployment-architecture)
12. [AI Architecture](#12-ai-architecture)
13. [Dependency Graph](#13-dependency-graph)
14. [Metrics](#14-metrics)

---

## 1. Executive Summary

AECai is a local-first document intelligence platform purpose-built for Architecture, Engineering, and Construction (AEC) firms. It processes documents through three engines -- Vanta, Aletheia, and Daedalus -- producing structured, verified, and searchable data entirely on-premises. The platform maintains zero cloud dependencies: all document processing, AI inference, vector storage, and workflow orchestration run within the firm's own infrastructure.

---

## 2. System Architecture

### High-Level Data Flow

```
Raw Documents --> Vanta (Parse / Classify / Enrich / Decompose / Index) --> Structured Output
                                                                                  |
                                                                                  v
                                                                           Aletheia (Verify)
                                                                                  |
                                                                                  v
                                                                           Daedalus (Retrieve / Generate)
```

### Component Overview

| Component                  | Location            | Scale                 | Description                                          |
|----------------------------|---------------------|-----------------------|------------------------------------------------------|
| **FastAPI Server**         | `aecai_server.py`   | 582 lines             | 29 API endpoints across 10 route modules, port 8443  |
| **Vanta Engine**           | `engine/vanta/`     | 13 files, 11,887 lines | Document intelligence pipeline                      |
| **Aletheia Engine**        | `engine/aletheia/`  | 6 files, 4,121 lines  | Verification, jurisdiction compliance, audit         |
| **Daedalus Engine**        | `engine/daedalus/`  | 6 files, 3,198 lines  | Semantic retrieval, reports, CAD/BIM scripts         |
| **Temporal Orchestration** | `temporal/`         | 19 files, 1,461 lines | 6 durable workflows, 18 activities                   |
| **Routes**                 | `routes/`           | 13 files, 1,401 lines | Extracted route modules for server endpoints         |

---

## 3. Engine: Vanta -- Document Intelligence

Vanta implements a 5-stage pipeline that transforms raw documents into structured, enriched, indexed data.

### Pipeline Stages

```
PARSE --> CLASSIFY --> ENRICH --> DECOMPOSE --> INDEX
```

1. **Parse** -- Extract text from 16+ file formats, chunk into processable segments, detect named entities.
2. **Classify** -- AI-first classification via Ollama with regex fallback; confidence-gated at 0.70.
3. **Enrich** -- Apply 5 enrichment plugins with circuit breaker protection.
4. **Decompose** -- Break documents into structural components for downstream analysis.
5. **Index** -- Embed and store in Qdrant vector collections for semantic retrieval.

### Module Breakdown

| File                   | Lines | Purpose                                                        |
|------------------------|-------|----------------------------------------------------------------|
| `vanta_core.py`        | 1,299 | Text extraction (16+ formats), chunking, entity detection      |
| `vanta_classify_v2.py` | 1,359 | AI-first classification (Ollama + regex fallback)              |
| `vanta_plugins.py`     | 1,098 | 5 enrichment plugins with circuit breaker                      |
| `vanta_pipeline.py`    | 1,155 | Pipeline orchestrator, SimulationAwareEngine integration       |
| `vanta_ai.py`          |   729 | Confidence-gated AI enhancement (threshold 0.70)               |
| `vanta_security.py`    | 1,802 | Input validation, PII, encryption, audit, compliance           |
| `vanta_simulation.py`  |   993 | Systems 5, 6, 8, 13, 15 + cross-engine coordinator            |
| `vanta_torsion.py`     |   885 | Systems 1--4: Adaptive computation, 30--70% compute savings    |
| `vanta_embed.py`       |   498 | Local embeddings (nomic-embed-text 768d, MiniLM 384d fallback) |
| `vanta_index.py`       |   664 | Qdrant vector store client (HTTP-based, zero pip deps)         |
| `vanta_geometry.py`    |   722 | DXF geometry extraction, AIA/NCS layer parsing                 |
| `vanta_batch.py`       |   682 | Parallel batch processing, content-hash dedup                  |
| `__init__.py`          |     1 | sys.path setup for cross-engine imports                        |

---

## 4. Engine: Aletheia -- Verification & Compliance

Aletheia provides a 3-step verification pipeline that validates structured output against schemas, jurisdiction-specific building codes, and produces tamper-evident audit certificates.

### Verification Steps

```
Schema Validation --> Jurisdiction Crossref --> Certification
```

1. **Schema Validation** -- 4-phase validation with quality scoring; safety-critical fields carry a 5x penalty multiplier.
2. **Jurisdiction Crossref** -- AHJ (Authority Having Jurisdiction) code adoption registry with edition comparison and cross-reference engine.
3. **Certification** -- Hash-chained audit ledger with certificate issuance and revocation.

### Module Breakdown

| File                       | Lines | Purpose                                                                          |
|----------------------------|-------|----------------------------------------------------------------------------------|
| `aletheia_schema.py`       |   861 | 4-phase validation, quality scoring, safety-critical 5x penalty                  |
| `aletheia_jurisdiction.py` | 1,162 | AHJ code adoption registry, edition comparison, crossref engine                  |
| `aletheia_ledger.py`       |   762 | SQLite hash-chained audit ledger, certificate issuance/revocation                |
| `aletheia_cli.py`          |   596 | CLI: validate, crossref, certify, verify, chain, stats                           |
| `aletheia_simulation.py`   |   739 | Systems 7, 10, 11, 12, 14, 16: CCN, QEC, anchors, Merkle, anomaly, counterfactual |
| `__init__.py`              |     1 | Package init                                                                     |

### Certification Levels

| Level      | Quality Threshold | Max Errors | Description                        |
|------------|-------------------|------------|------------------------------------|
| **Gold**   | >= 0.95           | 0          | Highest confidence, zero defects   |
| **Silver** | >= 0.80           | 0          | High confidence, zero defects      |
| **Bronze** | >= 0.60           | <= 2       | Acceptable confidence, minor issues|

---

## 5. Engine: Daedalus -- Retrieval & Automation

Daedalus provides semantic retrieval over indexed documents and generates actionable outputs including intelligence reports, Civil3D scripts, and Revit/Dynamo automation files.

### Module Breakdown

| File                     | Lines | Purpose                                              |
|--------------------------|-------|------------------------------------------------------|
| `daedalus_retrieve.py`   |   886 | Qdrant semantic search, jurisdiction/discipline/risk filters |
| `daedalus_report.py`     |   639 | Briefing, precedent, risk, and prediction reports    |
| `daedalus_civil3d.py`    |   625 | `.scr`/`.lsp` scripts for Civil3D                    |
| `daedalus_revit.py`      |   712 | `.journal`/`.dyn`/`.json` for Revit/Dynamo/IFC      |
| `daedalus_simulation.py` |   335 | Systems 9, 17: HolographicStore, TopologicalBraid   |
| `__init__.py`            |     1 | Package init                                         |

---

## 6. Simulation-Aware Systems

AECai incorporates 17 simulation-aware systems distributed across the three engines. These systems provide adaptive computation, self-improving detection, tamper detection, anomaly detection, and other advanced capabilities.

### Three-Pillar Distribution

| #  | System                     | Engine            | Class                      | Purpose                                      |
|----|----------------------------|-------------------|----------------------------|----------------------------------------------|
| 1  | Lazy Reality Scheduler     | Vanta (torsion)   | `TorsionEngine`            | Defer expensive ops on low-signal chunks     |
| 2  | Spin-Curvature Field       | Vanta (torsion)   | `TorsionField`             | Physics-inspired importance metadata         |
| 3  | Vortex Caching             | Vanta (torsion)   | `TorsionEngine`            | Hot-spot persistence                         |
| 4  | Chirality Feedback         | Vanta (torsion)   | `TorsionEngine`            | Bidirectional learning                       |
| 5  | Quantum Discrete Protocol  | Vanta (sim)       | `QuantumDiscreteProtocol`  | Deterministic batched messages               |
| 6  | Hierarchical Reality VM    | Vanta (sim)       | `HierarchicalRealityVM`    | Nested document contexts                     |
| 7  | Causal Consistency Network | Aletheia          | `CausalConsistencyNetwork` | Explainable causal chains                    |
| 8  | Memetic Evolution          | Vanta (sim)       | `MemeticEvolution`         | Self-improving detection patterns            |
| 9  | Holographic Store          | Daedalus          | `HolographicStore`         | Erasure-resilient storage                    |
| 10 | Quantum Error Corrector    | Aletheia          | `QuantumErrorCorrector`    | Multi-channel parity voting                  |
| 11 | Reality Anchor System      | Aletheia          | `RealityAnchorSystem`      | Known-true confidence cascading              |
| 12 | Temporal Merkle Tree       | Aletheia          | `TemporalMerkleTree`       | Unit-level tamper detection                  |
| 13 | Consciousness Scheduler    | Vanta (sim)       | `ConsciousnessScheduler`   | Attention-budget allocation                  |
| 14 | Simulation Escape Detector | Aletheia          | `SimulationEscapeDetector` | Anomaly detection                            |
| 15 | Irreducibility Detector    | Vanta (sim)       | `IrreducibilityDetector`   | Verbatim preservation                        |
| 16 | Counterfactual Logger      | Aletheia          | `CounterfactualLogger`     | Decision + alternative logging               |
| 17 | Topological Braid          | Daedalus          | `TopologicalBraid`         | Structural data segregation                  |

### Coordinator

`SimulationAwareEngine` in `vanta_simulation.py` serves as the cross-engine coordinator, composing `AletheiaSimulationSuite` and `DaedalusSimulationSuite` into a unified simulation layer.

---

## 7. API Architecture

The server exposes 29 endpoints across 10 route modules, all served via FastAPI on port 8443.

### Route Modules

| Module                    | Endpoints  | Purpose                                                  |
|---------------------------|------------|----------------------------------------------------------|
| `routes/process.py`       | 4          | Document processing (demo, standard, rich, training export) |
| `routes/documents.py`     | 2          | Browse processed outputs                                 |
| `routes/chat.py`          | 1 (+ page) | RAG-powered chat via Qdrant + Ollama SSE                |
| `routes/health.py`        | 1          | Service status                                           |
| `routes/leads.py`         | 4          | Lead capture + management                                |
| `routes/projects.py`      | 3          | Project CRUD                                             |
| `routes/feedback.py`      | 2          | User corrections                                         |
| `routes/jurisdictions.py` | 3          | Jurisdiction registry CRUD                               |
| `routes/workflows.py`     | 4          | Temporal workflow triggers                               |
| `routes/pages.py`         | 4          | Static HTML page serving                                 |

### Middleware Stack

```
Request --> CORS --> API Key Auth --> Security Headers --> Request Logging --> Route Handler
```

### Shared Infrastructure

- **`deps.py`** -- Dependency injection: `require_localhost` guard for admin endpoints, `rate_limit` middleware.
- **`models.py`** -- Pydantic request/response models shared across all route modules.

---

## 8. Workflow Architecture (Temporal)

AECai uses Temporal for durable workflow orchestration. When Temporal is unavailable, all workflows fall back to inline execution within the FastAPI process.

### Workflows

| Workflow                       | Activities                                                         | Timeout       |
|--------------------------------|--------------------------------------------------------------------|---------------|
| `DocumentPipelineWorkflow`     | process_standard, process_rich, process_training, index            | 10 min        |
| `VerificationWorkflow`         | validate_schema, crossref_jurisdiction, issue_certificate          | 5 min         |
| `IntelligenceReportWorkflow`   | retrieve_patterns, generate_report, civil3d_script, revit_script   | 15 min        |
| `BatchProcessWorkflow`         | discover_files, process_single_file                                | 60 min        |
| `RetrainWorkflow`              | ingest_documents, convert_training, train_model                    | 30/10/60 min  |
| `BatchOutreachWorkflow`        | draft_for_lead                                                     | 2 min/lead    |

### Infrastructure

- **Task Queue**: `aecai`
- **Dev Server**: `temporal server start-dev --db-filename temporal_dev.db`
- **Worker**: `python -m temporal.worker` (registers 6 workflows, 18 activities)
- **Web UI**: `http://localhost:8233`
- **Fallback**: Inline execution when Temporal is unavailable.

---

## 9. Data Architecture

All storage is local. No data leaves the host machine.

### Storage Layers

| Layer          | Technology   | Details                                                                      |
|----------------|--------------|------------------------------------------------------------------------------|
| **Vector**     | Qdrant       | 3 collections (`documents`, `geometry`, `jurisdictions`), 768-dim cosine similarity |
| **Relational** | SQLite       | Audit ledger (WAL mode, hash-chained)                                        |
| **Structured** | JSON / JSONL | Leads, feedback, projects, pipeline outputs, training data                   |
| **File System**| Local disk   | Document outputs in `data/outputs/`, training data in `data/training/`       |

---

## 10. Security Architecture

### Controls

| Domain               | Implementation                                                        |
|----------------------|-----------------------------------------------------------------------|
| **Input Validation** | Magic byte verification, extension whitelist, path traversal detection |
| **Authentication**   | Bearer token (`AECAI_API_KEY`), constant-time comparison              |
| **PII Protection**   | Detection + optional redaction                                        |
| **Encryption**       | AES-256 via Fernet                                                    |
| **Audit**            | HMAC-SHA256 signed, hash-chained entries                              |
| **Network**          | Admin endpoints localhost-only, rate limiting, security headers       |

### Compliance Frameworks

- NIST 800-53
- ISO 27001
- SOC 2
- GDPR
- CCPA
- HIPAA
- ITAR

---

## 11. Deployment Architecture

Deployment uses Docker Compose with 5 services. Ollama runs on the host for GPU acceleration. All containers run as non-root users with health checks enabled.

### Services

| Service        | Image                            | CPU  | Memory |
|----------------|----------------------------------|------|--------|
| Qdrant         | `qdrant/qdrant:v1.13.2`         | 2    | 2 GB   |
| Temporal       | `temporalio/auto-setup:1.26.2`  | 1    | 1 GB   |
| Temporal UI    | `temporalio/ui:2.31.2`          | 0.5  | 256 MB |
| AECai Server   | Custom (Python 3.11-slim)        | 2    | 4 GB   |
| AECai Worker   | Same image as Server             | 2    | 4 GB   |

---

## 12. AI Architecture

### Models and Capabilities

| Capability          | Model / Technique                                                              |
|---------------------|--------------------------------------------------------------------------------|
| **Classification**  | Ollama `llama3`, confidence-gated (threshold 0.70)                             |
| **Embeddings**      | `nomic-embed-text` (768d) via Ollama; `sentence-transformers` MiniLM (384d) fallback |
| **Chat**            | RAG via Qdrant (top 5 results, min_score 0.3) with Ollama SSE streaming       |
| **Fine-tuning**     | MLX LoRA on Apple Silicon (`llama3-8B-4bit`, 600 iterations)                   |

All AI inference runs locally. No API calls to external services.

---

## 13. Dependency Graph

```
engine/__init__.py (sys.path setup)
  |
  +-- engine/vanta/ (13 files)
  |     \-- vanta_simulation.py imports from:
  |           +-- engine/aletheia/aletheia_simulation.py
  |           \-- engine/daedalus/daedalus_simulation.py
  |
  +-- engine/aletheia/ (6 files, leaf -- no cross-engine deps)
  |
  \-- engine/daedalus/ (6 files, leaf -- no cross-engine deps)

aecai_server.py
  +-- routes/*.py
  |     \-- pipeline_ops.py
  |           +-- VantaPipeline
  |           +-- Aletheia modules
  |           \-- Daedalus modules
  |
  \-- temporal/ (when available)
```

Key observations:

- **Aletheia** and **Daedalus** are leaf modules with no cross-engine dependencies.
- **Vanta** is the only engine with cross-engine imports, limited to simulation composition in `vanta_simulation.py`.
- The server depends on all three engines through `pipeline_ops.py` and the route modules.

---

## 14. Metrics

| Metric                 | Value   |
|------------------------|---------|
| Total Python files     | ~99     |
| Total lines of code    | ~31,414 |
| API endpoints          | 29      |
| Route modules          | 10      |
| File formats supported | 16+     |
| Enrichment plugins     | 5       |
| Temporal workflows     | 6       |
| Temporal activities    | 18      |
| Qdrant collections     | 3       |
| Simulation systems     | 17      |
| Config parameters      | 31      |
| Tests                  | 554     |
| Test files             | 36      |

---

*ECHO-ARCH-001 v4.0 -- Echology, Inc. -- Internal*
