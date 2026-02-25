"""Shipping detection — poll GitHub for new tags and releases."""

import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone

from marketing.config import MONITORED_REPOS
from marketing.db import get_db, get_shipping_state, upsert_shipping_state, save_event


@dataclass
class ShippingEvent:
    repo: str
    event_type: str       # "tag" or "release"
    ref: str              # tag name
    title: str
    body: str = ""
    url: str = ""
    diff_summary: str = ""
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def _gh_api(endpoint: str) -> dict | list | None:
    """Call gh api and return parsed JSON, or None on failure."""
    try:
        result = subprocess.run(
            ["gh", "api", endpoint, "--paginate"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def _get_latest_tags(repo: str, limit: int = 5) -> list[dict]:
    """Fetch the most recent tags for a repo."""
    data = _gh_api(f"repos/{repo}/tags?per_page={limit}")
    if isinstance(data, list):
        return data
    return []


def _get_latest_release(repo: str) -> dict | None:
    """Fetch the latest release for a repo."""
    data = _gh_api(f"repos/{repo}/releases/latest")
    if isinstance(data, dict) and "tag_name" in data:
        return data
    return None


def _get_diff_summary(repo: str, old_tag: str, new_tag: str) -> str:
    """Fetch abbreviated diff between two tags."""
    data = _gh_api(f"repos/{repo}/compare/{old_tag}...{new_tag}")
    if not isinstance(data, dict):
        return ""

    files = data.get("files", [])
    summary_parts = [
        f"Commits: {data.get('total_commits', '?')}",
        f"Files changed: {len(files)}",
    ]
    for f in files[:10]:
        summary_parts.append(
            f"  {f.get('status', '?')} {f.get('filename', '?')} "
            f"(+{f.get('additions', 0)} -{f.get('deletions', 0)})"
        )
    if len(files) > 10:
        summary_parts.append(f"  ... and {len(files) - 10} more files")

    return "\n".join(summary_parts)


def check_for_new_shipping() -> list[ShippingEvent]:
    """Poll all monitored repos for new tags. Returns new shipping events."""
    db = get_db()
    events = []

    for repo in MONITORED_REPOS:
        state = get_shipping_state(db, repo)
        last_seen = state["last_seen_tag"] if state else None

        tags = _get_latest_tags(repo)
        if not tags:
            upsert_shipping_state(db, repo)
            continue

        latest_tag = tags[0]["name"]

        # First run — seed the state, don't generate content for existing tags
        if last_seen is None:
            upsert_shipping_state(db, repo, latest_tag)
            continue

        # No new tags
        if latest_tag == last_seen:
            upsert_shipping_state(db, repo)
            continue

        # New tag(s) found — collect all tags between last_seen and latest
        new_tags = []
        for tag in tags:
            if tag["name"] == last_seen:
                break
            new_tags.append(tag["name"])

        for tag_name in reversed(new_tags):
            # Try to get release notes
            release = _get_latest_release(repo)
            release_body = ""
            release_url = ""
            if release and release.get("tag_name") == tag_name:
                release_body = release.get("body", "")
                release_url = release.get("html_url", "")

            # Get diff from previous tag
            diff = _get_diff_summary(repo, last_seen, tag_name)

            event = ShippingEvent(
                repo=repo,
                event_type="tag",
                ref=tag_name,
                title=f"New tag: {tag_name}",
                body=release_body,
                url=release_url or f"https://github.com/{repo}/releases/tag/{tag_name}",
                diff_summary=diff,
            )
            events.append(event)

            # Persist to database
            save_event(
                db, repo=repo, event_type=event.event_type, ref=event.ref,
                title=event.title, body=event.body, url=event.url,
                diff_summary=event.diff_summary,
            )

        # Update state to latest
        upsert_shipping_state(db, repo, latest_tag)

    db.close()
    return events
