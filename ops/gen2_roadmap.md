# AECai Gen 2.0 — Product Roadmap

**Version:** 1.0
**Last updated:** 2026-02-14
**Owner:** AECai Engineering
**Timeline:** 18 months (6 phases)

---

## Executive Summary

AECai Gen 1.x delivered a working document-intelligence pipeline for the AEC (Architecture, Engineering, Construction) industry: file upload, AI-powered classification (Vanta), regulatory cross-referencing (Aletheia), vector retrieval and report generation (Daedalus), and a Temporal-orchestrated async workflow layer. The system runs as a single FastAPI server backed by JSONL flat files, Qdrant for vector search, and Ollama for local LLM inference.

Gen 2.0 transforms AECai from a capable single-tenant prototype into a production-grade, multi-tenant SaaS platform with enterprise security, real-time collaboration, enhanced intelligence, deep AEC-tool integrations, and mobile access. Each phase ships independently and maintains backward compatibility with the Gen 1.x API surface.

---

## Current Architecture (Gen 1.x)

```
                          +-----------+
                          |   Client  |
                          | (Browser) |
                          +-----+-----+
                                |
                          HTTPS :8443
                                |
                     +----------v-----------+
                     |   FastAPI Server      |
                     |   aecai_server.py     |
                     |   29 endpoints        |
                     |   IP allowlist auth   |
                     +--+------+------+------+
                        |      |      |
            +-----------+  +---+---+  +------------+
            |              |       |               |
    +-------v------+ +----v----+ +v-----------+ +--v---------+
    |    Vanta      | | Aletheia| |  Daedalus  | |  Temporal  |
    |  (Pipeline)   | | (Verify)| | (Retrieve) | | (Workflow) |
    |  classify     | | schema  | |  Qdrant    | |  6 flows   |
    |  enrich       | | xref    | |  reports   | | 18 activs  |
    |  decompose    | | ledger  | |  scripts   | |            |
    +-------+-------+ +----+----+ +-----+------+ +--+---------+
            |              |            |             |
            v              v            v             v
    +-------------------------------------------+  +--------+
    |            JSONL Flat Files                |  | SQLite |
    |  projects.json  feedback.jsonl  leads.jsonl|  | (temp) |
    +-------------------------------------------+  +--------+
```

**Strengths:** Fast iteration, single-binary deployment, rich AI pipeline, zero cloud dependencies.

**Limitations:** Single-tenant, no persistent auth, flat-file storage, no real-time push, no external integrations, no horizontal scaling.

---

## Target Architecture (Gen 2.0)

```
                    +------------------+     +-----------------+
                    |  Web App (SPA)   |     | Mobile (RN)     |
                    +--------+---------+     +--------+--------+
                             |                        |
                     HTTPS / WSS                 HTTPS / WSS
                             |                        |
                    +--------v------------------------v--------+
                    |              API Gateway                  |
                    |   /api/v1/*   rate-limit   JWT verify     |
                    +--------+----------------+----------------+
                             |                |
               +-------------v--+       +-----v--------------+
               | FastAPI Server  |       | WebSocket Server   |
               | (stateless x N) |       | room-based pub/sub |
               +-+----+----+----+       +-----+--------------+
                 |    |    |                  |
      +----------+  +-+--++ +--------+  +----+----+
      |             |     |          |  |         |
 +----v-----+ +----v--+ +v-------+ +v--v---+ +---v------+
 |   Vanta   | |Aletheia| |Daedalus| |Temporal| |Webhooks |
 |  Pipeline | | Verify | |Retrieve| |Orchestr| |  + SSE  |
 +----+------+ +---+----+ +---+----+ +---+----+ +---+-----+
      |            |           |          |          |
      v            v           v          v          v
 +----+------------+-----------+----------+----------+-----+
 |                      PostgreSQL                          |
 |  users | orgs | projects | documents | audit_logs        |
 |  Alembic-managed schema, row-level tenant isolation      |
 +----+-----------------------------------------------------+
      |
 +----v---------+   +------------+   +--------------+
 |   Qdrant     |   |   Redis    |   | Object Store |
 | (vectors)    |   | (cache,    |   | (S3/Minio    |
 |              |   |  rate-lim) |   |  documents)  |
 +--------------+   +------------+   +--------------+
```

---

## Phase 1 — Foundation (Months 1-3)

### Objectives

Replace flat-file storage with a relational database, implement proper authentication and authorization, establish API versioning, and lay the observability foundation for production operations.

### Key Deliverables

1. **PostgreSQL migration** — Replace all JSONL flat files (projects.json, feedback.jsonl, leads.jsonl) with an Alembic-managed relational schema.
   - Tables: `users`, `organizations`, `projects`, `documents`, `semantic_units`, `audit_logs`, `feedback`, `leads`
   - Alembic migration chain from zero state; no data loss for existing JSONL data (one-time import script)

2. **JWT authentication + refresh tokens + RBAC** — Replace IP-allowlist auth with industry-standard token auth.
   - Roles: `admin`, `engineer`, `viewer`, `auditor`
   - Access token (15 min) + refresh token (7 days) rotation
   - Permission matrix enforced at the route decorator level

3. **Organization-based multi-tenancy** — Row-level data isolation so multiple organizations share a single deployment.
   - Every database row carries an `org_id` foreign key
   - Middleware injects tenant context from JWT claims
   - Query filters enforced at the ORM layer (SQLAlchemy session events)

4. **API versioning** — Prefix all endpoints under `/api/v1/` with deprecation headers for the legacy unversioned paths.
   - `Deprecation` and `Sunset` response headers on legacy routes
   - Version negotiation via `Accept-Version` header (future-proofing)

5. **Structured logging + OpenTelemetry tracing** — Replace ad-hoc print/logger calls with structured JSON logs and distributed tracing.
   - `structlog` for JSON log output with correlation IDs
   - OpenTelemetry SDK with Jaeger/OTLP exporter
   - Trace context propagated through Temporal workflows

6. **Prometheus metrics endpoint** — `/metrics` exposing request latency, pipeline throughput, error rates, and queue depth.

### Architecture Changes

- New dependency: `asyncpg`, `sqlalchemy[asyncio]`, `alembic`, `python-jose`, `passlib`, `structlog`, `opentelemetry-sdk`
- `aecai_server.py` router split into versioned route modules under `routes/v1/`
- Database connection pool managed via SQLAlchemy async engine
- Auth middleware added to FastAPI dependency chain

### Success Metrics

| Metric | Target |
|--------|--------|
| Multi-tenant isolation | 3+ orgs on single instance, zero cross-org data leaks |
| Auth overhead | < 100 ms per request (JWT verify + RBAC check) |
| API backward compatibility | 100% of Gen 1.x endpoints still functional via legacy prefix |
| Migration safety | Zero data loss during JSONL-to-PostgreSQL migration |
| Observability | 100% of requests traced, structured logs in production |

### Dependencies

- PostgreSQL 16+ (local dev via Docker Compose, managed instance for prod)
- Redis (introduced here for session blocklist; expanded in Phase 2)

---

## Phase 2 — Real-Time & Integration (Months 3-6)

### Objectives

Enable real-time push notifications for long-running operations, provide webhook integration points for external systems, and implement organization-level rate limiting.

### Key Deliverables

1. **WebSocket endpoint** — `/ws/projects/{project_id}` for live processing status.
   - Room-based pub/sub: clients subscribe to a project room
   - Events: `processing.started`, `processing.stage_changed`, `processing.completed`, `processing.error`
   - Connection authentication via JWT query parameter

2. **Configurable webhooks** — Organizations register webhook URLs for specific events.
   - Events: `document.processed`, `verification.completed`, `report.generated`, `training.finished`
   - Retry with exponential backoff (1s, 2s, 4s, 8s, 16s, max 5 retries)
   - HMAC-SHA256 signature verification (`X-AECai-Signature` header)
   - Webhook management API: create, list, test, delete, view delivery logs

3. **SSE progress streaming** — `GET /api/v1/stream/{task_id}` for all long-running operations.
   - Server-Sent Events with progress percentage, stage name, and ETA
   - Works as a lightweight alternative to WebSocket for simple integrations

4. **Redis-backed rate limiting** — Per-organization request quotas.
   - Sliding-window rate limiter using Redis sorted sets
   - Configurable per plan tier (e.g., free: 100 req/min, pro: 1000 req/min)
   - `X-RateLimit-Remaining` and `Retry-After` response headers

### Architecture Changes

- WebSocket manager class with Redis pub/sub backend for horizontal scaling
- Webhook delivery as a Temporal workflow (guaranteed delivery, retry, dead-letter)
- Redis becomes a required service (rate limiting + WebSocket pub/sub + cache)

### Success Metrics

| Metric | Target |
|--------|--------|
| Push latency | < 500 ms from event to client delivery |
| Webhook delivery rate | 99.9% successful delivery within 5 retries |
| Cross-org data leaks | Zero (WebSocket rooms enforce tenant isolation) |
| Rate limiter accuracy | Within 1% of configured limits under concurrent load |

### Dependencies

- Phase 1 (JWT auth, PostgreSQL, multi-tenancy)
- Redis 7+ (pub/sub, rate limiting, caching)

---

## Phase 3 — Enhanced Intelligence (Months 4-8)

### Objectives

Significantly improve retrieval quality, add model versioning and experimentation infrastructure, and enable proactive intelligence alerts.

### Key Deliverables

1. **Hybrid RAG pipeline** — Combine Qdrant vector search with BM25 keyword search using Reciprocal Rank Fusion (RRF).
   - BM25 index maintained in PostgreSQL using `tsvector` / `ts_rank`
   - RRF formula: `score = sum(1 / (k + rank_i))` across vector and keyword result sets
   - Configurable fusion weight parameter per query type

2. **Cross-encoder re-ranking** — After RRF fusion, apply a cross-encoder (sentence-transformers) to re-rank the top-k candidates.
   - Model: `cross-encoder/ms-marco-MiniLM-L-6-v2` (default, configurable)
   - Re-rank top 50 candidates down to final top 10
   - Latency budget: < 200 ms for re-ranking pass

3. **ML model registry** — Track classifier and embedding model versions, with A/B testing framework.
   - Registry table: `model_versions` (model_name, version, artifact_path, metrics, active)
   - A/B traffic splitting at the pipeline level (e.g., 90/10 between classifier v2.1 and v2.2)
   - Automatic metric collection (precision, recall, latency) per model version

4. **Proactive alerts** — System-initiated notifications when external conditions change.
   - Jurisdiction code adoption changes (e.g., "Henderson NV adopted IBC 2024 on 2026-07-01")
   - Standard supersession notifications (e.g., "ASTM A992-22 superseded by A992-25")
   - Configurable alert channels: in-app, email, webhook

5. **Active learning loop** — Low-confidence classifications flagged for human review; corrections feed retraining.
   - Confidence threshold configurable per organization (default: 0.7)
   - Review queue UI: show unit text, model prediction, confidence, and allow correction
   - Corrections accumulated into fine-tuning dataset; retrain triggered via Temporal workflow

### Architecture Changes

- New `intelligence` module alongside existing engine modules
- BM25 index as PostgreSQL materialized view with GIN index on `tsvector`
- Model registry backed by PostgreSQL + object storage for artifacts
- Alert scheduler as a Temporal cron workflow (daily check for supersessions)

### Success Metrics

| Metric | Target |
|--------|--------|
| RAG relevance (MRR@10) | 15% improvement over vector-only baseline |
| Classifier precision | 90%+ on top-5 document types |
| Re-ranking latency | < 200 ms for top-50 candidates |
| Alert latency | < 24 hours from source publication to user notification |
| Active learning adoption | 50%+ of flagged units reviewed within 48 hours |

### Dependencies

- Phase 1 (PostgreSQL for BM25 index and model registry)
- Phase 2 (webhooks for alert delivery, SSE for review queue notifications)

---

## Phase 4 — Document Management (Months 6-10)

### Objectives

Transform AECai from a processing pipeline into a document management platform with versioning, collaboration, and approval workflows native to the AEC industry.

### Key Deliverables

1. **Document versioning with semantic diff** — Track every version of a processed document and highlight meaningful changes.
   - Version table: `document_versions` (document_id, version_number, content_hash, semantic_units_snapshot, created_by, created_at)
   - Semantic diff algorithm: align units by embedding similarity, flag added/removed/modified units
   - Diff UI: side-by-side view with change highlighting at the semantic-unit level

2. **Inline annotations and threaded comments** — Users can annotate specific text ranges within a document.
   - Annotation model: (document_id, version, start_offset, end_offset, author, thread_id)
   - Threaded replies within an annotation
   - Mention support (@user) with notification delivery

3. **Configurable approval workflows** — Status progression: `draft` -> `pending_review` -> `approved` -> `published`.
   - Workflow definition per project (configurable required approvers, auto-escalation timeout)
   - Approval actions recorded in audit log with digital signature (Aletheia ledger integration)
   - API: submit for review, approve, reject with comment, publish

4. **Jurisdiction comparison engine** — Answer questions like "What changes if Henderson adopts IBC 2024?"
   - Compare two jurisdiction profiles and produce a delta report
   - Highlight affected documents in the user's project
   - Integration with Aletheia cross-reference engine for standard mapping

### Architecture Changes

- New `document_versions` and `annotations` tables in PostgreSQL
- Approval workflow modeled as a Temporal long-running workflow with signal-based state transitions
- Semantic diff as a compute-intensive task run via Temporal activity (cached after first computation)

### Success Metrics

| Metric | Target |
|--------|--------|
| Version history | 100% of processed documents have version trail |
| Diff computation | < 2 seconds for documents up to 500 semantic units |
| Approval workflow adoption | 80%+ of organizations using approval flow within 3 months of launch |
| Annotation engagement | Average 3+ annotations per reviewed document |

### Dependencies

- Phase 1 (PostgreSQL, auth/RBAC for approver roles)
- Phase 2 (WebSocket for real-time annotation sync, notifications)
- Phase 3 (embedding similarity for semantic diff alignment)

---

## Phase 5 — Ecosystem (Months 8-14)

### Objectives

Extend AECai beyond the browser with CAD/BIM tool integrations, a public API with SDKs, construction-platform connectors, and a plugin marketplace.

### Key Deliverables

1. **CAD/BIM execution agents** — Direct integration with Civil3D and Revit.
   - Civil3D COM API agent: Windows service that accepts Daedalus-generated scripts and executes them in Civil3D
   - Revit .NET API agent: Windows service for Revit automation (PatternToRevit pipeline)
   - Agent protocol: gRPC with mutual TLS, job queue via Temporal

2. **Public REST API with auto-generated SDKs** — First-class API for external developers.
   - OpenAPI 3.1 specification auto-generated from FastAPI routes
   - SDKs: Python (PyPI), JavaScript/TypeScript (npm), C# (.NET NuGet)
   - API key management UI, usage dashboard, and billing integration

3. **Construction platform integrations** — Procore and Autodesk Construction Cloud.
   - Procore: project sync (bidirectional), daily log ingestion, RFI auto-classification
   - Autodesk Construction Cloud: document sync, BIM 360 model data extraction
   - OAuth2 connection flow managed per organization

4. **Notification bots** — Slack and Microsoft Teams integrations.
   - Configurable triggers: processing complete, verification failed, approval needed, alert fired
   - Slash commands for quick status checks (`/aecai status`, `/aecai search <query>`)

5. **Plugin marketplace** — Community-contributed plugins with sandboxed execution.
   - Plugin SDK with typed interface (input schema, output schema, manifest.json)
   - WASM sandbox for untrusted plugin execution (Wasmtime runtime)
   - Marketplace UI: browse, install, rate, review
   - Revenue sharing model for paid plugins

### Architecture Changes

- New `integrations` module for Procore/ACC/Slack/Teams connectors
- gRPC service definition for CAD agent communication
- WASM runtime embedded in the plugin execution path (opt-in per plugin)
- SDK generation as a CI pipeline step (openapi-generator)

### Success Metrics

| Metric | Target |
|--------|--------|
| Third-party integrations | 3+ live integrations (Procore, ACC, Slack) |
| SDK adoption | 10+ external developers using published SDKs |
| Marketplace plugins | 5+ community-contributed plugins |
| CAD agent reliability | 95%+ successful script execution rate |

### Dependencies

- Phase 1 (auth for API keys, multi-tenancy for org-scoped integrations)
- Phase 2 (webhooks as the notification backbone)
- Phase 4 (approval workflows for integration-triggered actions)

---

## Phase 6 — Enterprise (Months 12-18)

### Objectives

Achieve enterprise-grade security certifications, high availability, and mobile access to position AECai for large-organization deployments.

### Key Deliverables

1. **Encryption at rest** — AES-256-GCM encryption for all stored documents and PII.
   - Envelope encryption: data encryption key (DEK) per document, key encryption key (KEK) in HSM/KMS
   - Transparent decryption at the application layer
   - Key rotation support without re-encrypting all data (re-wrap DEKs with new KEK)

2. **SAML SSO + SCIM provisioning** — Enterprise identity integration.
   - SAML 2.0 IdP-initiated and SP-initiated SSO
   - SCIM 2.0 for automated user provisioning and deprovisioning
   - JIT (just-in-time) user creation on first SSO login
   - Integration tested with Okta, Azure AD, and OneLogin

3. **SOC 2 Type II certification** — Complete the audit process.
   - Trust Service Criteria: Security, Availability, Confidentiality
   - Evidence collection automated via audit log queries and infrastructure-as-code
   - Continuous compliance monitoring dashboard

4. **High-availability deployment** — Multi-region with zero-downtime deploys.
   - PostgreSQL streaming replication (primary + hot standby, async replica in secondary region)
   - Blue/green deployment strategy with automatic rollback on health check failure
   - Qdrant cluster mode (3-node minimum) with replication factor 2
   - Temporal cluster with Cassandra/PostgreSQL persistence (multi-node)
   - Target: 99.95% uptime SLA

5. **Mobile applications** — iOS and Android apps built with React Native.
   - Core features: document upload (camera + file picker), processing status, search, report viewing
   - Offline upload queue: documents queued locally and synced when connectivity returns
   - Push notifications for processing completion and approval requests
   - Biometric authentication (Face ID / fingerprint)

6. **Edge processing agent** — Lightweight agent for field offices with intermittent connectivity.
   - Local document ingestion and queuing
   - Sync-when-online with conflict resolution (last-write-wins with audit trail)
   - Subset of Vanta pipeline runs locally (parse + classify); full enrichment deferred to cloud

### Architecture Changes

- KMS integration (AWS KMS / HashiCorp Vault) for key management
- SAML middleware (python3-saml) added to auth chain
- Kubernetes deployment manifests with Helm charts for HA configuration
- React Native mobile app repository (separate repo, shared API client)
- Edge agent as a standalone Go binary with embedded SQLite

### Success Metrics

| Metric | Target |
|--------|--------|
| SOC 2 certification | Type II report issued |
| Uptime SLA | 99.95% measured over trailing 90 days |
| Failover time | < 30 seconds for database failover |
| Mobile app availability | Published in App Store and Google Play Store |
| Edge agent sync reliability | 99.9% eventual delivery of queued documents |

### Dependencies

- Phase 1 (PostgreSQL, auth infrastructure as the foundation for SSO)
- Phase 2 (WebSocket/SSE for mobile real-time updates)
- Phase 4 (document versioning for edge sync conflict resolution)

---

## Migration Strategy

Each phase is designed to ship independently while building on the infrastructure established by prior phases. The key principle is **additive change with backward compatibility** -- no phase removes functionality that earlier phases or external consumers depend on.

### Incremental Shipping Model

1. **Phase 1 ships first and unlocks everything else.** The PostgreSQL migration and auth system are prerequisites for all subsequent phases. A one-time JSONL-to-PostgreSQL migration script runs during the deployment window. Legacy unversioned API endpoints continue to work via a compatibility shim that maps to `/api/v1/` handlers.

2. **Phases 2 and 3 can overlap.** Real-time features (Phase 2) and intelligence improvements (Phase 3) are largely independent. WebSocket/SSE infrastructure does not depend on hybrid RAG, and vice versa. Teams can work in parallel after Phase 1 lands.

3. **Phase 4 depends on Phases 1-3.** Document versioning requires PostgreSQL (Phase 1), real-time sync requires WebSocket (Phase 2), and semantic diff requires embeddings (Phase 3). This is the integration phase where the platform becomes cohesive.

4. **Phase 5 extends outward.** Ecosystem integrations are additive and can ship incrementally (e.g., Procore integration can ship before Revit agent). Each integration is a self-contained module with its own test suite.

5. **Phase 6 hardens for enterprise.** Security certifications and HA deployment are the final layer. SOC 2 evidence collection begins in Phase 1 (audit logs) and accumulates through all phases.

### Database Migration Approach

- Alembic manages all schema changes as a linear migration chain
- Every migration is reversible (`upgrade` and `downgrade` functions)
- Migrations run automatically on deploy via a pre-start hook
- Large data migrations (e.g., JSONL import) run as background Temporal workflows with progress tracking

### Feature Flags

- All new features behind feature flags (LaunchDarkly or equivalent)
- Gradual rollout per organization (canary -> 10% -> 50% -> 100%)
- Kill switch for any feature that causes production issues

---

## Risk & Mitigation

### 1. Database Migration Risk

**Risk:** Data loss or corruption during JSONL-to-PostgreSQL migration. Extended downtime during cutover.

**Mitigation:**
- Write migration script with comprehensive validation: row counts, checksum verification, and bidirectional comparison
- Run migration in shadow mode first (dual-write to both JSONL and PostgreSQL for 2 weeks)
- Maintain JSONL as read-only fallback for 30 days post-migration
- Practice migration on production-sized dataset in staging environment at least 3 times before actual cutover
- Cutover window: 15 minutes maximum; automated rollback if validation fails

### 2. Auth System Complexity

**Risk:** JWT implementation introduces security vulnerabilities (token leakage, insufficient rotation, RBAC bypass).

**Mitigation:**
- Use battle-tested libraries (`python-jose`, `passlib`) rather than custom crypto
- Mandatory security review of auth middleware before Phase 1 ships
- Automated penetration testing in CI (OWASP ZAP baseline scan)
- Token blocklist in Redis for immediate revocation capability
- Rate limiting on auth endpoints to prevent brute-force attacks
- Regular third-party security audit (quarterly starting Phase 1)

### 3. Backward Compatibility

**Risk:** API versioning breaks existing client integrations. Site pages (index.html, app.html, process.html, chat.html) stop working.

**Mitigation:**
- Legacy endpoint shim: all Gen 1.x paths redirect to `/api/v1/` equivalents with `301` + `Deprecation` header
- Automated backward-compatibility test suite: replay recorded Gen 1.x request/response pairs against new server
- Deprecation timeline: legacy endpoints supported for 6 months minimum after versioned endpoints ship
- Client-side graceful degradation: site pages detect API version and adapt

### 4. Performance Regression

**Risk:** PostgreSQL queries slower than flat-file reads for small datasets. Hybrid RAG adds latency. Multi-tenant query filters add overhead.

**Mitigation:**
- Benchmark suite: automated latency tests for all critical paths (upload, process, search, verify)
- Performance budget: no endpoint may regress more than 20% vs Gen 1.x baseline
- PostgreSQL query optimization: proper indexing (GIN for full-text, B-tree for foreign keys, partial indexes for tenant isolation)
- Connection pooling via PgBouncer for high-concurrency scenarios
- Caching layer (Redis) for frequently accessed data (project lists, user profiles, search results)
- Load testing with realistic concurrent user counts before each phase ships (k6 or Locust)

### 5. Scope Creep

**Risk:** 18-month roadmap with 6 phases is ambitious. Feature creep in any phase delays subsequent phases.

**Mitigation:**
- Each phase has a hard scope boundary defined by the deliverables listed above
- Phase gates: a phase ships when its success metrics are met, not when all wish-list items are complete
- Two-week sprint cycles with demo at end of each sprint
- Monthly roadmap review to re-prioritize based on customer feedback and market changes
- "Phase 0" items (bug fixes, tech debt, developer experience) allocated 20% of each sprint

---

## Appendix: Technology Stack Summary

| Layer | Gen 1.x | Gen 2.0 |
|-------|---------|---------|
| Web framework | FastAPI | FastAPI (versioned routes) |
| Database | JSONL flat files | PostgreSQL 16 + Alembic |
| Vector store | Qdrant | Qdrant (cluster mode) |
| Cache / rate limit | None | Redis 7 |
| Auth | IP allowlist | JWT + RBAC + SAML SSO |
| Orchestration | Temporal (single node) | Temporal (cluster) |
| LLM | Ollama (local) | Ollama (local) + cloud fallback |
| Observability | Python logging | structlog + OpenTelemetry + Prometheus |
| CI/CD | GitHub Actions | GitHub Actions + Helm + blue/green |
| Mobile | None | React Native (iOS/Android) |
| Edge | None | Go agent with SQLite |

---

*This document is a living roadmap. Phase timelines and deliverables will be refined at each monthly review based on engineering velocity, customer feedback, and market conditions.*
