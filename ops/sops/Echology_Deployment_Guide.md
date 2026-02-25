# AECai Deployment & Operations Guide

| Field   | Value            |
|---------|------------------|
| Version | 4.0              |
| Date    | February 2026    |
| Author  | Echology, Inc.   |

> **Supersedes:** `Echology_Deployment_Guide_v3.0.docx` and `VANTA_SOP_v1.3_Deployment_Guide.docx`. Those documents are now stale and should not be referenced.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Installation](#2-installation)
3. [Configuration](#3-configuration)
4. [Local Development Startup](#4-local-development-startup)
5. [Docker Compose Production Deployment](#5-docker-compose-production-deployment)
6. [Service Dependencies & Health Checks](#6-service-dependencies--health-checks)
7. [Makefile Targets](#7-makefile-targets)
8. [Testing](#8-testing)
9. [Data Directories](#9-data-directories)
10. [Backup & Recovery](#10-backup--recovery)
11. [Troubleshooting](#11-troubleshooting)
12. [Security Considerations](#12-security-considerations)

---

## 1. Prerequisites

### Hardware (Recommended)

| Component | Specification |
|-----------|---------------|
| Machine | Mac Mini M4 Pro (8-core, 16 GB RAM) |
| Internal storage | 512 GB SSD |
| External SSD | 1 TB (projects + Qdrant) |
| External HDD | 4 TB (backups) |
| Architecture | Apple Silicon required for MLX fine-tuning |

### Software

| Dependency | Notes |
|------------|-------|
| macOS | Tested on Apple Silicon M-series |
| Python 3.11 | Via Homebrew: `brew install python@3.11` |
| Docker Desktop | For Qdrant, Temporal |
| Ollama | For local LLM inference |
| Tesseract | For OCR: `brew install tesseract` |

### Python Dependencies (from requirements.txt)

| Category | Packages |
|----------|----------|
| Server | fastapi, uvicorn, python-multipart, aiofiles |
| Document extraction | PyMuPDF, python-docx, ezdxf |
| OCR | pytesseract, Pillow |
| Embeddings | sentence-transformers, torch, transformers |
| Temporal | temporalio |
| Testing | pytest, httpx |

---

## 2. Installation

```bash
# Clone repository
git clone git@github.com:aecai-io/aecai.git
cd aecai

# Create Python virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create data directories
mkdir -p data/outputs data/training data/aecai_training data/drafts data/tmp

# Install Ollama models
ollama pull llama3
ollama pull nomic-embed-text
```

---

## 3. Configuration

All configuration lives in `config.py` (the `_Config` class). There are 31 parameters, every one of which can be overridden with an environment variable using the `AECAI_` prefix.

| Category | Variable | Default |
|----------|----------|---------|
| Server | `AECAI_HOST` | `127.0.0.1` |
| Server | `AECAI_PORT` | `8443` |
| Server | `AECAI_MAX_UPLOAD_MB` | `50` |
| Server | `AECAI_RATE_LIMIT_SECONDS` | `10` |
| Server | `AECAI_JSON_BODY_LIMIT_KB` | `1024` |
| AI | `AECAI_OLLAMA_HOST` | `http://localhost:11434` |
| AI | `AECAI_OLLAMA_MODEL` | `llama3` |
| AI | `AECAI_EMBED_MODEL` | `nomic-embed-text` |
| AI | `AECAI_AI_THRESHOLD` | `0.70` |
| Chunking | `AECAI_CHUNK_SIZE` | `2000` |
| Chunking | `AECAI_CHUNK_OVERLAP` | `200` |
| Qdrant | `AECAI_QDRANT_HOST` | `localhost` |
| Qdrant | `AECAI_QDRANT_PORT` | `6333` |
| Temporal | `AECAI_TEMPORAL_HOST` | `localhost:7233` |
| Temporal | `AECAI_TEMPORAL_TASK_QUEUE` | `aecai` |
| Aletheia | `AECAI_ALETHEIA_REGISTRY` | `~/.echology/aletheia/jurisdictions.json` |
| Aletheia | `AECAI_ALETHEIA_LEDGER` | `~/.echology/aletheia/ledger.db` |
| Security | `AECAI_API_KEY` | *(empty = auth disabled)* |
| Logging | `AECAI_LOG_LEVEL` | `INFO` |

---

## 4. Local Development Startup

Services must be started in the order below. Each numbered step should run in its own terminal unless noted otherwise.

```bash
# 1. Start Qdrant (Docker)
docker compose up -d qdrant

# 2. Ensure Ollama is running
ollama serve  # or: brew services start ollama

# 3. Start Temporal dev server
temporal server start-dev --db-filename temporal_dev.db

# 4. Start AECai worker (new terminal)
source .venv/bin/activate
python -m temporal.worker

# 5. Start AECai server (new terminal)
source .venv/bin/activate
python aecai_server.py
```

> **Note:** The server takes 10-15 seconds to load all Vanta modules on startup. This is expected behavior.

### Access Points

| Service | URL |
|---------|-----|
| AECai Web | http://localhost:8443 |
| AECai App | http://localhost:8443/app |
| Temporal UI | http://localhost:8233 |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

## 5. Docker Compose Production Deployment

Five services are defined in `docker-compose.yml`:

| Service | Image | Port(s) | Resources |
|---------|-------|---------|-----------|
| Qdrant | `qdrant/qdrant:v1.13.2` | 6333 / 6334 | 2 CPU / 2 GB |
| Temporal | `temporalio/auto-setup:1.26.2` | 7233 | 1 CPU / 1 GB |
| Temporal UI | `temporalio/ui:2.31.2` | 8233 | 0.5 CPU / 256 MB |
| AECai Server | Custom build | 8443 | 2 CPU / 4 GB |
| AECai Worker | Same image, `python -m temporal.worker` | -- | 2 CPU / 4 GB |

```bash
# Full stack
docker compose up -d

# Check health
docker compose ps
curl http://localhost:8443/api/health
```

### Key Points

- **Ollama** runs on the host (GPU-accelerated). Containers reach it via `host.docker.internal:11434`.
- Containers run as a non-root user (`aecai`).
- All services have health checks and resource limits.

### Volumes

| Mount | Purpose |
|-------|---------|
| `./data:/app/data` | Persistent data (outputs, training, logs) |
| `./data/qdrant_storage:/qdrant/storage` | Qdrant persistent storage |
| `temporal_data` (named volume) | Temporal SQLite DB |

---

## 6. Service Dependencies & Health Checks

### Startup Dependency Chain

```
Qdrant (healthy) ──┐
                    ├──> AECai Server
Temporal (healthy) ─┤
                    └──> AECai Worker

Temporal (healthy) ──> Temporal UI
```

### Health Check Endpoints

| Service | Check |
|---------|-------|
| Qdrant | `curl http://localhost:6333/healthz` |
| Temporal | gRPC on port 7233 |
| AECai | `GET /api/health` -- returns status of all subsystems |

---

## 7. Makefile Targets

| Target | Command | Description |
|--------|---------|-------------|
| `make help` | -- | Show all targets |
| `make lint` | `ruff check . && ruff format --check .` | Lint + format check |
| `make format` | `ruff format .` | Auto-format |
| `make test` | `pytest tests/ -v --timeout=30` | Run all 554 tests |
| `make test-cov` | `coverage run -m pytest ...` | Tests + coverage report |
| `make audit` | `pip-audit -r requirements.txt` | Dependency vulnerability check |
| `make check` | lint + test-cov + audit | Full CI check |
| `make smoke` | smoke-up + smoke-test + smoke-down | Integration tests with Docker services |

---

## 8. Testing

554 tests across 36 test files (6,562 lines).

```bash
# All tests
make test

# With coverage
make test-cov

# Specific test file
python -m pytest tests/test_vanta_core.py -v

# Integration tests (requires Qdrant + Temporal)
make smoke
```

### CI Pipeline (GitHub Actions)

Three jobs run on every push and pull request:

1. **Lint** -- `ruff check` and `ruff format --check`
2. **Test** -- Full test suite with Qdrant and Temporal services
3. **Audit** -- `pip-audit` dependency vulnerability scan

Timeout: 15 minutes.

---

## 9. Data Directories

```
data/
├── outputs/                  # Per-document JSON outputs
│   ├── *_standard.json       #   Frontend metrics
│   ├── *_rich.json           #   Full semantic envelope
│   └── *_training.jsonl      #   Training records per unit
├── training/                 # Raw training corpus
├── aecai_training/           # Converted training data + LoRA adapters + GGUF
├── drafts/                   # Outreach drafts
├── qdrant_storage/           # Qdrant persistent storage
├── tmp/                      # Temporary upload files
├── leads.jsonl               # Sales leads
├── feedback.jsonl            # User corrections
├── projects.json             # Project metadata
├── pipeline_outputs.jsonl    # Aggregated results
└── server.log                # Server activity log
```

---

## 10. Backup & Recovery

All data is local. Back up the following regularly:

| What | Path |
|------|------|
| Qdrant storage | `data/qdrant_storage/` |
| Temporal state | Named volume `temporal_data` |
| Aletheia ledger | `~/.echology/aletheia/ledger.db` |
| Jurisdiction registry | `~/.echology/aletheia/jurisdictions.json` |
| Document outputs | `data/outputs/` |
| Training data | `data/aecai_training/` |

---

## 11. Troubleshooting

| Symptom | Cause / Resolution |
|---------|-------------------|
| Server slow to start | Normal. Vanta module loading takes 10-15 seconds. |
| Ollama not responding | Run `ollama serve` and verify the model is pulled (`ollama list`). |
| Qdrant connection error | Daedalus returns an error dict; the server handles it gracefully. Check that the Docker container is running. |
| Temporal unavailable | The server falls back to inline processing (no durable execution). Restart the Temporal container. |
| OCR not working | Install Tesseract: `brew install tesseract`. |
| System Python conflicts | Use the `.venv` with Python 3.11. The system Python is 3.9.6 and is not compatible (Temporal requires >= 3.10). |

---

## 12. Security Considerations

- **Admin endpoints** are restricted to localhost.
- **API key authentication** is controlled by `AECAI_API_KEY`. When the value is empty, authentication is disabled.
- **All data stays local** -- zero cloud dependencies.
- **Docker containers** run as a non-root user (`aecai`).
- **File locking** (`fcntl`) prevents concurrent corruption of shared data files.
- **Magic byte verification** is performed on all uploaded files to prevent disguised payloads.

---

*Copyright 2025-2026 Echology, Inc. All rights reserved.*
