"""Settings for the marketing agent."""

import os
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent  # echology/
MARKETING_DIR = Path(__file__).resolve().parent     # echology/marketing/
DB_PATH = MARKETING_DIR / "marketing.db"
VOICE_DIR = MARKETING_DIR / "voice_corpus"
BLOG_DIR = ROOT_DIR / "docs" / "blog"
BLOG_INDEX = ROOT_DIR / "docs" / "blog.html"
DOCS_DIR = ROOT_DIR / "docs"

# ── Repos to Monitor ──────────────────────────────────────────────────────
MONITORED_REPOS = [
    "echology-io/decompose",
    "echology-io/aecai",
]

# ── Agent Settings ─────────────────────────────────────────────────────────
MAX_RETRIES = 2           # Quality gate retry limit before marking needs_review
POLL_INTERVAL = 1800      # 30 minutes in seconds (for daemon mode)

# ── Twitter (Phase 2) ─────────────────────────────────────────────────────
# Load from environment when ready
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET", "")
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "")
