# Tasks: Workflow — Local Tracking

**Last synced from Notion:** 2026-02-21 (14 backlog + 5 research + 6 sub-items → complete synced; full .01-.25 audit)
**Notion DB:** https://www.notion.so/2682973f06dc8115b832efbe10cf82ef
**Data Source ID:** 2682973f-06dc-8190-aa33-000bef5503cd

Update this file locally, then batch-sync to Notion. Status values: `Completed`, `In Progress`, `New`, `On Hold`, `Cancelled`. Bucket values: `.24 Complete`, `.25 Archive`, `.03 Backlog`, `.05 Research`.

---

## IN PROGRESS

| Task | Bucket | Notion ID | Notes |
|------|--------|-----------|-------|
| Prepare Decompose launch plan (HN, Reddit, LinkedIn) | .14 Launch | `30e2973f-06dc-8131-a71f-e74bfd34767d` | Posts drafted, schedule ready. HN window Sun/Mon 7-9 AM ET |

---

## ACTIONABLE GAPS (from 2026-02-21 audit)

These need action. Create Notion tasks or fix directly.

### Critical — Before Launch

| # | Gap | Repo | Action | Status |
|---|-----|------|--------|--------|
| G1 | Sitemap missing 4 blog posts | echology | Added 3 posts to `docs/sitemap.xml` | DONE |
| G2 | Blog index duplicate entry | echology | Removed duplicate from `docs/blog.html` | DONE |
| G3 | Version mismatch pyproject vs ClawHub | echology | PyPI is 0.1.1 (correct). Fixed LAUNCH.md typo (said 0.1.2) | DONE |

### Medium — Fix Soon

| # | Gap | Repo | Action | Status |
|---|-----|------|--------|--------|
| G4 | Qdrant storage path mismatch | aecai | Made configurable via `QDRANT_STORAGE` env var in docker-compose + start_temporal.sh | DONE |
| G5 | Git remote URL typo (double dot) | kylevines | FALSE POSITIVE — repo is actually named `kylevines.` on GitHub, URL was correct | N/A |
| G6 | Decompose import fragile (.pth link) | aecai | Added `decompose-mcp>=0.1.1` to requirements.txt + pyproject.toml | DONE |
| G7 | hello-fly/ untracked, not gitignored | aecai | Added to .gitignore | DONE |
| G8 | .gitignore uncommitted | kylevines | Committed and pushed | DONE |

### Low — Cleanup

| # | Gap | Repo | Action | Status |
|---|-----|------|--------|--------|
| G9 | docs/sops/ missing | aecai | Removed stale path, added `AECAI_INGEST_DIRS` env var | DONE |
| G10 | data/aecai_training/ gitignore stale | aecai | Consolidated to single `data/aecai_training/` entry | DONE |
| G11 | Server docstring says "Cloudflare Tunnel" | aecai | Updated to "Fly.io or local network" | DONE |
| G12 | echology-unified-theory.md tracked publicly | kylevines | Gitignored + untracked (kept on disk) | DONE |
| G13 | No CHANGELOG | echology | Created CHANGELOG.md with v0.1.0 + v0.1.1 | DONE |
| G14 | Personal blog has only 1 post | kylevines | Replaced placeholder with real "Why I Build" post | DONE |

---

## COMPLETED

| Task | Bucket | Notion ID | Completed |
|------|--------|-----------|-----------|
| Release Decompose standalone library (v0.1.2 on PyPI, MCP Registry, ClawHub) | .24 Complete | `30e2973f-06dc-8170-9aa5-f299534a5d50` | 2026-02 |
| Build RBS Policy QC demo (insurance three-tier extraction pipeline) | .24 Complete | `30e2973f-06dc-813f-9c99-cb0e43364a46` | 2026-02 |
| Build Polymarket trading system (5 strategies, paper + live dashboards) | .24 Complete | `30e2973f-06dc-815f-b635-d5c726003bfb` | 2026-02 |
| Execute repo separation (aecai / echology) | .24 Complete | `30e2973f-06dc-81b9-b342-c79820db87a0` | 2026-02 |
| Write unified theory + positioning realignment | .24 Complete | `30e2973f-06dc-81ce-9d3e-de1c84c5c409` | 2026-02 |
| Implement filter_for_llm() in Decompose library | .24 Complete | `30e2973f-06dc-8137-9be6-ea0bc8a6aa16` | 2026-02 |
| Add structural entity validators to Vanta core | .24 Complete | `30e2973f-06dc-81a3-ad6d-d7e6c0aa4c06` | 2026-02 |
| Implement deterministic-first document classification | .24 Complete | `30e2973f-06dc-8137-9406-e8cd8fcd795c` | 2026-02 |
| Add Decompose pre-filter to Vanta pipeline (Stage 1.5) | .24 Complete | `30e2973f-06dc-8199-b0f0-f2066afb9850` | 2026-02 |
| Build Temporal workflow integration (6 workflows, 18 activities) | .24 Complete | `30e2973f-06dc-81eb-a924-c9732b526b34` | 2026-02 |
| Build FastAPI server (aecai_server.py, port 8443) | .24 Complete | `30e2973f-06dc-81a5-87e7-ee526317e814` | 2026-02 |
| Build kylevines.com personal site | .24 Complete | `30e2973f-06dc-8164-b2ed-d395d8be8a7f` | 2026-02 |
| Build Aletheia verification engine | .24 Complete | `30e2973f-06dc-81c1-b85a-d2e1f27cbf25` | 2026-02 |
| Build Daedalus retrieval and report generation engine | .24 Complete | `30e2973f-06dc-81e4-ac3b-c24e2fb28741` | 2026-02 |
| Setup SSH Access: Windows Surface to Mac Mini M4 Pro | .24 Complete | `2742973f-06dc-80c0-bece-e96268ab9749` | 2025-09 |
| Migrate proven CLI system from Windows to macOS | .24 Complete | `065dd8f7-600e-44df-a5fd-dacbffe37ba8` | 2025-09 |
| Benchmark performance improvements (Mac mini) | .24 Complete | `29acc3a0-22ad-4fc3-b0d5-433511ea6627` | 2025-09 |
| Install and configure JetBrains suite | .24 Complete | `0be0fdba-fd20-49d9-8dd3-9c246a477ca5` | 2025-09 |
| Design and develop homepage with brand story | .24 Complete | `258e632e-f945-4891-9b30-9d1c73291b96` | 2025-09 |
| Set up blog homepage with category filters | .24 Complete | `2da3f10f-e7bf-4309-848a-95f47168911e` | 2025-09 |
| Build VANTA CLI architecture | .24 Complete | `3f6842e2-7aa8-490c-83ca-1dec70e08efb` | 2025-11 |
| Define input formats (PDF, DOCX, TXT, CSV, DWG, DXF, RVT, IFC) | .24 Complete | `676a6319-2059-43f4-ada0-b84eb67f89c0` | 2025-09 |
| Task, deadline, person, and entity detection (EchoInput) | .24 Complete | `c17ce22e-024b-41e9-992b-fc0f085d420f` | 2025-09 |
| Smart chunking and data processing (EchoPipeline) | .24 Complete | `fddcf37d-1a17-49bf-bec1-bcda41a3a214` | 2025-09 |
| Implement `vanta redact` (PII/BII anonymization) | .24 Complete | `02f46f67-4cba-47e4-9f45-8fdce54dd2e8` | 2025-09 |
| Test with industry datasets (Testing & QA) | .24 Complete | `46010d16-2b0b-4fc9-8898-5e456c963195` | 2025-09 |
| Large-file stress tests (Testing & QA) | .24 Complete | `aa8463dc-2f32-471f-b3ea-69289262f33c` | 2025-09 |
| Create benchmark suite for performance testing | .24 Complete | `0fb96f0b-8faf-42ff-8432-f89dd066fb87` | 2025-09 |
| Documentation completeness audit | .24 Complete | `08bcdb4e-8516-4fbc-9b24-3aa67f95a56f` | 2025-09 |
| Build dashboards: Exec KPIs, Product Ops, Sales, Legal, Finance | .24 Complete | `16bc9f99-bf20-424c-917c-391b02a3b0d9` | 2025-09 |
| Structure operations environment (Namecheap, ProtonMail, Ghost, Notion) | .24 Complete | `5b04747c-74f2-46a2-935b-dc073c3e8270` | 2025-09 |
| Develop investor pitch deck (GTM) | .24 Complete | `3a324f1d-c1ff-4464-b86b-029bf0453f07` | 2025-09 |
| Define & document pipeline | .24 Complete | `26a2973f-06dc-80c0-a310-e2f766fc4d34` | 2026-02 |
| Core Framework Development (Vanta engine) | .24 Complete | `ca5c3728-b763-4246-867b-7f24b97c11c9` | 2026-02 |
| EchoPipeline Module (now vanta_pipeline.py) | .24 Complete | `3536e5bc-9bdc-4c82-8701-f393d112018e` | 2026-02 |
| EchoSecure Module (now vanta_security.py) | .24 Complete | `fd2ee49d-f14d-4ffb-bec2-e08db9286050` | 2026-02 |
| EchoDeck Module (now daedalus_report.py) | .24 Complete | `7a4b87d3-e5bc-4598-b585-ee9462cb876d` | 2026-02 |
| EchoAgents Module (now vanta_plugins.py) | .24 Complete | `3615eae3-58b0-489a-8e8b-0600a2bacb19` | 2026-02 |
| Testing & QA (577 AECai + 63 Echology tests) | .24 Complete | `cd40812f-88dc-49ca-ba0f-3c33aa0c18a1` | 2026-02 |
| Create databases: Tasks, Projects, CRM, Content | .24 Complete | `4eef6e63-7842-467c-9e5c-210e8256a272` | 2026-02 |
| Integrate task management (Scrum/Kanban via Notion) | .24 Complete | `784ad13a-a79e-4d03-a343-c1aefb0a602c` | 2026-02 |
| Notion Command Center | .24 Complete | `94fc321c-bb3b-4113-abf1-6addbe5a91d3` | 2026-02 |
| Operations Stack (Namecheap, ProtonMail, Notion, GitHub) | .24 Complete | `9efd0228-733b-44bc-a87c-7d3eaf680ccf` | 2026-02 |
| Write Aletheia vision one-pager | .24 Complete | `05f9e6f6-1ad4-49f2-940c-2e7ee7742649` | 2026-02 |
| Social bios (LinkedIn, GitHub, echology.io) | .24 Complete | `27d2973f-06dc-8096-91f7-d6eabd9334c8` | 2026-02 |
| Add author bios (Kyle Vines on echology.io + kylevines.com) | .24 Complete | `065cac10-da76-4a3b-ad4a-34d4814cee39` | 2026-02 |
| Build Lazy Reality Scheduler (LRS) — vanta_torsion.py:281 | .24 Complete | `3fe21e38-7b43-4155-926b-382c6578f5da` | 2026-02 |
| Build Quantum-Discrete Network Protocol (QDNP) — vanta_simulation.py:95 | .24 Complete | `690b60f6-1413-46d9-b165-c88afb457ee2` | 2026-02 |
| Build Hierarchical Reality Virtual Machine (HRVM) — vanta_simulation.py:237 | .24 Complete | `04d2e980-12b7-4e01-910d-07da3d3c8482` | 2026-02 |
| Implement Causal Consistency Networks (CCN) — aletheia_simulation.py:43 | .24 Complete | `c30a6eae-081d-4e1c-a9b6-b45f8ec27fcc` | 2026-02 |
| Build Memetic Algorithm Resource Evolution (MARE) — vanta_simulation.py:401 | .24 Complete | `b834d686-3b32-485f-a44d-ed867b9e252f` | 2026-02 |
| CAD/BIM vector extraction (vanta_geometry.py, daedalus_revit.py, daedalus_civil3d.py) | .24 Complete | `0b741187-8456-48ba-b6e2-eb5ca08f43c6` | 2026-02 |
| DWT/DXF CLI pipeline utilities (vanta_geometry.py) | .24 Complete | `7ed5dffb-fede-4887-a23d-3eac2da57098` | 2026-02 |
| Provide Docker images for enterprise deployment (Dockerfile + docker-compose.yml) | .24 Complete | `717e7ac8-d895-4b70-9736-84b44f95462a` | 2026-02 |
| Package Vanta for pip (PyPI) — pyproject.toml v3.1.0 | .24 Complete | `a9ce97b5-949f-4608-a421-775beed30888` | 2026-02 |
| Industry-specific agent bundles (5 plugins: Standards, PII, Timeline, Financial, Contract) | .24 Complete | `3c6e2813-df0c-4dbd-a72a-74fc2c61d2c2` | 2026-02 |
| Security whitepaper (local-first air-gap in vanta_security.py) | .24 Complete | `5460e708-46f4-4a9a-bb3c-09f549077c54` | 2026-02 |

---

## ON HOLD — Backlog (.03)

| Task | Notion ID | Category |
|------|-----------|----------|
| open s-corp (c?) | `2682973f-06dc-810b-824e-e9a11f9355a4` | Legal/Entity |
| Entity Formation | `ad51c514-6df2-4245-a44e-52381b05b25e` | Legal/Entity |
| Obtain EIN | `b4b0a8c3-adc5-4c38-b002-4baadc584c95` | Legal/Entity |
| NC foreign qualification | `795ed8b4-88e0-494e-b846-76a34a818397` | Legal/Entity |
| 409A valuation preparation | `c114b368-8d81-4fdb-8357-cfecae9d101e` | Legal/Entity |
| Business insurance (liability, cyber, E&O) | `95204402-b0d6-4aec-8c3a-cbb4613d9362` | Legal/Entity |
| Legal Documentation (parent) | `c08d9a94-1bb7-4f9a-8c42-3ff0869bbd70` | Legal/Entity |
| Schema Registry & Contracts | `2807a7bd-f80b-46e7-a4fa-2c71a1ca3732` | Legal/Entity |
| Content Calendar | `2872973f-06dc-8096-b992-ce41e0d58d33` | Marketing |
| VSL video sales letter | `28f2973f-06dc-80c1-9f78-e607fdfe688b` | Marketing |
| YT: Why start now? | `27d2973f-06dc-809a-89b6-f3fd2ba2743a` | Marketing |
| Marketing Strategy (parent) | `ea21bf72-5324-4546-8cb7-0e0d5cdc70be` | Marketing |
| Business Development (parent) | `f6aeb4b3-90fe-4a9b-a9fd-90afff775ecd` | Business |
| Business Strategy (parent) | `7073dcdf-d695-4751-93ae-b74355e0d9e4` | Business |
| Create ECSIT Systemization Offer sheet | `5a5f7a38-0910-417a-b6cb-aee5e4b874fb` | ECSIT |
| Uptime status page setup | `90c8af36-d779-456b-a520-a6f52782f6b0` | Ops |
| Implement `vanta export` (JSON → CSV/XLSX/Markdown) | `14571093-5b75-42fe-94dd-153736688f64` | Product |
| Implement `vanta diff` (compare doc revisions) | `2b28c63b-6d68-49b5-a37c-744e10bdd971` | Product |
| Cross-OS install smoke tests (Mac, Windows, Linux) | `0db3f7ba-4cc3-470b-8b31-a0daaa542736` | Product |
| Create install docs for Windows, Mac, Linux | `874138a5-cf4f-4837-9d28-42ab0d037af7` | Product |
| Apple Developer enrollment & code-signing certificates | `0c5f7607-c05e-4f3d-a2b6-419194e1e286` | Distribution |
| Code signing and release trust implementation | `457a5133-aa4c-493b-91ee-e6dee949ffdd` | Distribution |
| Package for Homebrew or other CLI channels | `fb1653a1-0e5b-4fe2-90f8-5d785d1e066c` | Distribution |
| Professional proposal document generation (EchoDeck) | `7cf01a96-3223-4c69-9af0-a6754a9dc6f5` | Product |
| Generate SOPs and slide decks from pipeline outputs (EchoDeck) | `dcc8b604-ecc2-447c-af8c-c8e61a10aa23` | Product |
| Auto-attach certification reports in decks (EchoDeck) | `356edcd2-11de-4f43-8833-5c88259c7079` | Product |
| Redaction policy documentation (EchoLog) | `24c53ea5-2b5d-4a4d-a9e6-568480b32852` | Product |
| Telemetry guardrails (opt-in vs opt-out) (EchoLog) | `b07a20e2-9bf1-4fa6-a3b6-b687ad9fffbf` | Product |
| Conduct buyer interviews (5-10 per target market) | `09a374cf-14c0-43f8-a55e-23c007daae06` | Business |
| Start list-building with waitlist signup | `0b190b91-d4fd-4176-83ae-e5bd23a4a402` | Business |
| Define success criteria for beta users | `1c595237-ab06-4f64-ac8b-80e7dccc4f9a` | Business |
| Define funding ask ($1M-$2.5M Seed) | `16c2e363-86b3-47cf-839f-9433877bc480` | Business |
| Design email sequences (cold, follow-up, nurture) | `1ba8c36c-1afe-404b-ab47-f17afe8ce644` | Business |

---

## ON HOLD — Research (.05)

*All 5 SimArch prototypes moved to COMPLETED — fully implemented in AECai engine.*

### Blockchain / Aletheia Anchoring (future work)

| Task | Notion ID | Category |
|------|-----------|----------|
| Define blockchain integration rationale | `cb545390-636a-4fe0-8cc3-d118dbd46c7c` | Web3 |
| Write "local-first + chain-anchored" principle | `82e966ce-f135-4348-a688-044bf2089531` | Web3 |
| Draft cross-industry compliance reviews (MiCA, SEC, OFAC) | `15360132-00c4-4c72-b89f-e5219690f465` | Web3 |
| Create enterprise DAO governance templates | `42a8db8d-c7a6-41fb-9139-2559b60166fb` | Web3 |
| Pick success metrics (verifiability, latency, fees, ops burden) | `0173c3c4-0ffe-4c5e-97fe-e7c6a33b4280` | Web3 |
| Compare L2s for anchoring/payments (rollups vs alt-L1) | `07536d1f-e91d-49e7-8666-5271d71baafc` | Web3 |
| Decide primary L2 for anchors/payments; backup chain | `68fc38ea-f98e-4740-a4d6-39ee6f627ed7` | Web3 |
| Define testnet strategy (one per environment) | `3554519f-3248-4792-ab44-10ca2dca9915` | Web3 |
| Implement cross-chain temporal consensus prototype | `d408c7dc-0635-4f57-9f88-a5002a82dbe6` | Web3 |
| Choose DID method compatible with local use (DID:key / DID:web) | `1a3b4cee-368a-42f3-ada5-d2819e4b5087` | Web3 |
| Issue/verify VCs locally; optionally anchor VC hashes on-chain | `f3336135-7539-4da0-8d23-ea34524fa2ba` | Web3 |

### Aletheia CLI — Blockchain Anchoring (Inbox)

| Task | Notion ID | Category |
|------|-----------|----------|
| Design anchor contract: store (hash, timestamp, metadata) | `558938f6-dade-4f6f-a0e3-30a43fb73936` | Web3 |
| Add CLI: `aletheia certify --anchor` | `0d1dedf4-2613-4668-87e7-a2b918a1f122` | Web3 |
| Implement cross-chain anchors (Aletheia) | `1a3d2e9a-1258-40a1-ad89-2c6278fc7232` | Web3 |
| Specify state-root hashing for Aletheia ledger snapshots | `e225d71d-26ca-433e-a409-b8094089a117` | Web3 |
| Write verifier CLI: `aletheia verify --proof <bundle>` | `b604356c-b9ef-4723-93bc-c24d57011424` | Web3 |
| Define VCs for: dataset cert, reviewer identity, organization role | `8bbb7dd7-35a9-469d-9e15-a0e234fedb03` | Web3 |
| Build DID integration for reviewer identity in Aletheia | `972a0aec-0f3d-4387-8b99-a30003a29147` | Web3 |

---

## ARCHIVE

| Task | Notion ID |
|------|-----------|
| Test (empty) | `4d9d4d1c-f96c-448e-90c3-333b23b7ee83` |
| (empty/template) | `2682973f-06dc-81c8-a125-ccd770f09d40` |

---

## TEST HEALTH (as of 2026-02-21)

| Repo | Tests | Pass | Fail | Duration |
|------|-------|------|------|----------|
| AECai | 577 | 577 | 0 | 29.2s |
| Echology | 63 | 63 | 0 | 0.03s |
| **Total** | **640** | **640** | **0** | **29.2s** |

---

## SYNC PROTOCOL

1. Edit this file locally (change status, add tasks, mark gaps done)
2. Run Claude: "sync TASKS.md to Notion" — batch-update changed rows by Notion ID
3. Update `Last synced` date at top

### Notion Property Mapping
- `Status` (select): Completed, In Progress, New, On Hold, Cancelled
- `Bucket` (select): .01-.25 (see Notion for full list)
- `Status 1` (status): Not started, In progress, Done
- When marking complete: set Status=Completed, Bucket=.24 Complete, Status 1=Done
