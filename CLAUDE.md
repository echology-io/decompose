# Echology — Project Context

## Organization

```
Echology, Inc. (parent company)
├── AECai      — main product (proprietary, ~/aecai)
├── Decompose  — open-source library (this repo, src/decompose/)
└── RBS Demo   — insurance QC demo (~/rbs-demo)
```

## This Repository

This repo serves dual purpose:
1. **Decompose library** (`src/decompose/`) — published to PyPI as `decompose-mcp`
2. **Company operations** (`ops/`, `marketing/`) — SOPs, deployment, training, outreach

The GitHub remote is `echology-io/decompose`. The local clone is named `echology/`.

## Key Paths

- `src/decompose/` — Decompose library source (the published package)
- `ops/sops/` — Standard operating procedures (markdown tracked, docx gitignored)
- `ops/training/` — MLX model training scripts (also copied to aecai/training/)
- `ops/site/` — Static HTML pages (aecai/site/ is the canonical copy with images)
- `marketing/` — Marketing automation, voice corpus, reddit content

## Cross-Repo Dependencies

- **AECai depends on Decompose**: `decompose-mcp>=0.2.0` in aecai/pyproject.toml
- **AECai imports**: `decompose_text()`, `filter_for_llm()`, `chunk_text()` from this library
- **Shared data**: `~/.echology/aletheia/` (jurisdictions registry, audit ledger)
- **Training scripts**: `ops/training/` is the original; `aecai/training/` has copies with local paths

## Versioning

- **Decompose**: SemVer in `pyproject.toml` (currently 0.2.0). Bump for each PyPI release.
- **Version string** also in `src/decompose/__init__.py` and `src/decompose/core.py` — keep in sync.

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v        # 76 tests, <0.1s
ruff check src/ tests/
```

## Rules

- No LLM dependencies in decompose — pure regex + heuristics only
- No external API calls except user-specified URLs in `decompose_url`
- Patterns backported from AECai must have tests before merge
- Keep stdlib-only (except `mcp` for the server interface)
