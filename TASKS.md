# Tasks: Workflow — Local Tracking

**Last synced from Notion:** 2026-02-21 (14 backlog + 5 research → complete synced)
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

---

## ON HOLD — Research (.05)

*All 5 SimArch prototypes moved to COMPLETED — fully implemented in AECai engine.*

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
