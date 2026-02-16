"""Settings and credentials for the marketing agent."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from marketing directory
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent  # echology/
MARKETING_DIR = Path(__file__).resolve().parent     # echology/marketing/
DB_PATH = MARKETING_DIR / "marketing.db"
VOICE_DIR = MARKETING_DIR / "voice_corpus"
BLOG_DIR = ROOT_DIR / "docs" / "blog"
BLOG_INDEX = ROOT_DIR / "docs" / "blog.html"
DOCS_DIR = ROOT_DIR / "docs"

# ── API Keys ───────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Twitter (Phase 2)
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET", "")
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "")

# ── Repos to Monitor ──────────────────────────────────────────────────────
MONITORED_REPOS = [
    "echology-io/decompose",
    "echology-io/aecai",
]

# ── Agent Settings ─────────────────────────────────────────────────────────
MAX_RETRIES = 2           # Quality gate retry limit before marking needs_review
POLL_INTERVAL = 1800      # 30 minutes in seconds (for daemon mode)

# ── Decompose MCP Server ──────────────────────────────────────────────────
DECOMPOSE_MCP_CMD = "/Users/kylevines/lab/.venv/bin/python"
DECOMPOSE_MCP_ARGS = ["-m", "decompose", "--serve"]
