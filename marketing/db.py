"""SQLite schema and CRUD helpers for the marketing agent."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from marketing.config import DB_PATH

_SCHEMA = """
CREATE TABLE IF NOT EXISTS shipping_state (
    repo TEXT PRIMARY KEY,
    last_checked TEXT NOT NULL,
    last_seen_tag TEXT
);

CREATE TABLE IF NOT EXISTS shipping_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo TEXT NOT NULL,
    event_type TEXT NOT NULL,
    ref TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    url TEXT,
    diff_summary TEXT,
    detected_at TEXT NOT NULL,
    processed INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipping_event_id INTEGER REFERENCES shipping_events(id),
    channel TEXT NOT NULL,
    title TEXT,
    body TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    quality_score REAL,
    quality_notes TEXT,
    created_at TEXT NOT NULL,
    published_at TEXT,
    published_url TEXT,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    action TEXT NOT NULL,
    content_id INTEGER REFERENCES content(id),
    details TEXT
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_db() -> sqlite3.Connection:
    """Open (and initialize if needed) the marketing database."""
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.executescript(_SCHEMA)
    return db


# ── Shipping state ─────────────────────────────────────────────────────────

def get_shipping_state(db: sqlite3.Connection, repo: str) -> dict | None:
    row = db.execute("SELECT * FROM shipping_state WHERE repo = ?", (repo,)).fetchone()
    return dict(row) if row else None


def upsert_shipping_state(db: sqlite3.Connection, repo: str, last_seen_tag: str | None = None):
    now = _now()
    existing = get_shipping_state(db, repo)
    if existing:
        if last_seen_tag is not None:
            db.execute("UPDATE shipping_state SET last_checked = ?, last_seen_tag = ? WHERE repo = ?",
                       (now, last_seen_tag, repo))
        else:
            db.execute("UPDATE shipping_state SET last_checked = ? WHERE repo = ?", (now, repo))
    else:
        db.execute("INSERT INTO shipping_state (repo, last_checked, last_seen_tag) VALUES (?, ?, ?)",
                   (repo, now, last_seen_tag))
    db.commit()


# ── Shipping events ───────────────────────────────────────────────────────

def save_event(db: sqlite3.Connection, repo: str, event_type: str, ref: str,
               title: str, body: str = "", url: str = "", diff_summary: str = "") -> int:
    cur = db.execute(
        "INSERT INTO shipping_events (repo, event_type, ref, title, body, url, diff_summary, detected_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (repo, event_type, ref, title, body, url, diff_summary, _now()),
    )
    db.commit()
    return cur.lastrowid


def mark_event_processed(db: sqlite3.Connection, event_id: int):
    db.execute("UPDATE shipping_events SET processed = 1 WHERE id = ?", (event_id,))
    db.commit()


def get_unprocessed_events(db: sqlite3.Connection) -> list[dict]:
    rows = db.execute("SELECT * FROM shipping_events WHERE processed = 0 ORDER BY id").fetchall()
    return [dict(r) for r in rows]


# ── Content ────────────────────────────────────────────────────────────────

def save_content(db: sqlite3.Connection, shipping_event_id: int, channel: str,
                 body: str, title: str = "", status: str = "draft",
                 metadata: dict | None = None) -> int:
    cur = db.execute(
        "INSERT INTO content (shipping_event_id, channel, title, body, status, created_at, metadata) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (shipping_event_id, channel, title, body, status, _now(),
         json.dumps(metadata) if metadata else None),
    )
    db.commit()
    return cur.lastrowid


def update_content_status(db: sqlite3.Connection, content_id: int, status: str,
                          published_url: str | None = None):
    if published_url:
        db.execute("UPDATE content SET status = ?, published_at = ?, published_url = ? WHERE id = ?",
                   (status, _now(), published_url, content_id))
    else:
        db.execute("UPDATE content SET status = ? WHERE id = ?", (status, content_id))
    db.commit()


def update_content_quality(db: sqlite3.Connection, content_id: int,
                           score: float, notes: str):
    db.execute("UPDATE content SET quality_score = ?, quality_notes = ? WHERE id = ?",
               (score, notes, content_id))
    db.commit()


def get_pending_content(db: sqlite3.Connection) -> list[dict]:
    rows = db.execute(
        "SELECT c.*, se.repo, se.ref, se.title as event_title "
        "FROM content c JOIN shipping_events se ON c.shipping_event_id = se.id "
        "WHERE c.status IN ('draft', 'needs_review') ORDER BY c.id"
    ).fetchall()
    return [dict(r) for r in rows]


def get_all_content(db: sqlite3.Connection, limit: int = 50) -> list[dict]:
    rows = db.execute(
        "SELECT c.*, se.repo, se.ref, se.title as event_title "
        "FROM content c JOIN shipping_events se ON c.shipping_event_id = se.id "
        "ORDER BY c.id DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_content_stats(db: sqlite3.Connection) -> list[dict]:
    rows = db.execute(
        "SELECT channel, status, COUNT(*) as count FROM content GROUP BY channel, status"
    ).fetchall()
    return [dict(r) for r in rows]


# ── Audit log ──────────────────────────────────────────────────────────────

def log_action(db: sqlite3.Connection, action: str, content_id: int | None = None,
               details: dict | None = None):
    db.execute(
        "INSERT INTO audit_log (timestamp, action, content_id, details) VALUES (?, ?, ?, ?)",
        (_now(), action, content_id, json.dumps(details) if details else None),
    )
    db.commit()
