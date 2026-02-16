"""Channel publishers — blog commit, LinkedIn draft, Twitter stub, newsletter stub."""

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from marketing.config import BLOG_DIR, BLOG_INDEX, ROOT_DIR, DOCS_DIR
from marketing.db import get_db, save_content, update_content_status, log_action


# ── Blog ───────────────────────────────────────────────────────────────────

_BLOG_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Echology</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title} — Echology">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://echology.io/blog/{slug}">
    <meta property="article:published_time" content="{date}">
    <meta name="twitter:card" content="summary">
    <link rel="stylesheet" href="../style.css">
    <style>
        .post-body {{ max-width: 720px; margin: 0 auto; }}
        .post-body h2 {{ font-size: 24px; font-weight: 700; margin: 48px 0 16px; letter-spacing: -0.3px; }}
        .post-body h3 {{ font-size: 18px; font-weight: 700; margin: 32px 0 12px; }}
        .post-body p {{ font-size: 16px; color: var(--muted); line-height: 1.75; margin-bottom: 20px; }}
        .post-body p strong {{ color: var(--fg); }}
        .post-body p code {{ background: var(--code-bg); padding: 2px 6px; border-radius: 3px; font-size: 14px; color: var(--accent); }}
        .post-body blockquote {{
            border-left: 3px solid var(--accent);
            padding: 12px 20px;
            margin: 24px 0;
            background: var(--code-bg);
            border-radius: 0 6px 6px 0;
        }}
        .post-body blockquote p {{ color: var(--fg); margin: 0; font-size: 15px; }}
        .post-body ul, .post-body ol {{ color: var(--muted); font-size: 16px; line-height: 1.75; margin-bottom: 20px; padding-left: 24px; }}
        .post-body li {{ margin-bottom: 8px; }}
        .post-body .code-block {{ margin: 24px 0; }}
        .post-meta {{ text-align: center; margin-bottom: 48px; }}
        .post-meta .date {{ font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: 1.5px; }}
        .post-meta .reading {{ font-size: 13px; color: var(--muted); margin-top: 4px; }}
        .post-body a {{ text-decoration: underline; text-underline-offset: 2px; }}
    </style>
</head>
<body>
    <nav>
        <div class="container">
            <a href="/" class="logo">echology<span>.</span></a>
            <button class="nav-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')">&#9776;</button>
            <div class="nav-links">
                <a href="/about">About</a>
                <a href="/aecai">AECai</a>
                <a href="/decompose">Decompose</a>
                <a href="/blog" class="active">Blog</a>
                <a href="/contact">Contact</a>
            </div>
        </div>
    </nav>

    <section class="hero">
        <div class="container container--narrow">
            <h1>{h1_line1}<br><span>{h1_line2}</span></h1>
            <p class="sub">{subtitle}</p>
            <div class="post-meta">
                <div class="date">{date_display}</div>
                <div class="reading">{reading_time} min read</div>
            </div>
        </div>
    </section>

    <section>
        <div class="container post-body">
{body_html}
        </div>
    </section>

    <footer>
        <div class="container">
            <div class="copy">&copy; 2025-2026 Echology, Inc.</div>
            <div class="footer-links">
                <a href="https://github.com/echology-io">GitHub</a>
                <a href="/about">About</a>
                <a href="/contact">Contact</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""

_BLOG_INDEX_ENTRY = """\
                <a href="/blog/{slug}" class="post-item">
                    <div class="post-date">{date_display}</div>
                    <div class="post-title">{title}</div>
                    <div class="post-excerpt">{excerpt}</div>
                </a>"""


def _estimate_reading_time(text: str) -> int:
    """Estimate reading time in minutes (250 wpm)."""
    words = len(text.split())
    return max(1, round(words / 250))


def _slugify(title: str) -> str:
    """Convert title to URL slug."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s-]+", "-", slug).strip("-")
    return slug


def commit_blog_post(
    title: str,
    subtitle: str,
    body_html: str,
    excerpt: str,
    description: str,
    shipping_event_id: int,
    slug: str | None = None,
    h1_line1: str | None = None,
    h1_line2: str | None = None,
) -> str:
    """Write blog HTML, update index, commit, and push. Returns the blog URL."""
    if not slug:
        slug = _slugify(title)
    if not h1_line1:
        words = title.split()
        mid = len(words) // 2
        h1_line1 = " ".join(words[:mid]) if mid > 0 else title
        h1_line2 = " ".join(words[mid:]) if mid > 0 else ""
    if not h1_line2:
        h1_line2 = ""

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    date_display = now.strftime("%B %d, %Y").replace(" 0", " ")
    reading_time = _estimate_reading_time(body_html)

    # Render the full HTML page
    html = _BLOG_TEMPLATE.format(
        title=title,
        description=description,
        slug=slug,
        date=date_str,
        date_display=date_display,
        h1_line1=h1_line1,
        h1_line2=h1_line2,
        subtitle=subtitle,
        reading_time=reading_time,
        body_html=body_html,
    )

    # Write the post file
    post_path = BLOG_DIR / f"{slug}.html"
    post_path.write_text(html)

    # Update the blog index — prepend new entry after <div class="post-list">
    index_html = BLOG_INDEX.read_text()
    new_entry = _BLOG_INDEX_ENTRY.format(
        slug=slug, date_display=date_display, title=title, excerpt=excerpt,
    )
    index_html = index_html.replace(
        '<div class="post-list">',
        f'<div class="post-list">\n{new_entry}',
    )
    BLOG_INDEX.write_text(index_html)

    # Git commit and push
    subprocess.run(
        ["git", "add", str(post_path), str(BLOG_INDEX)],
        cwd=str(ROOT_DIR), capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-m", f"blog: {title}"],
        cwd=str(ROOT_DIR), capture_output=True,
    )
    subprocess.run(
        ["git", "push"],
        cwd=str(ROOT_DIR), capture_output=True,
    )

    blog_url = f"https://echology.io/blog/{slug}"

    # Record in database
    db = get_db()
    content_id = save_content(
        db, shipping_event_id, "blog", body_html,
        title=title, status="published",
        metadata={"slug": slug, "url": blog_url},
    )
    update_content_status(db, content_id, "published", published_url=blog_url)
    log_action(db, "publish_blog", content_id, {"slug": slug, "url": blog_url})
    db.close()

    return blog_url


# ── LinkedIn (drafts only) ─────────────────────────────────────────────────

def save_linkedin_draft(content: str, shipping_event_id: int) -> int:
    """Save a LinkedIn draft to the database. Returns content ID."""
    db = get_db()
    content_id = save_content(db, shipping_event_id, "linkedin", content, status="draft")
    log_action(db, "save_linkedin_draft", content_id)
    db.close()
    return content_id


# ── Twitter (Phase 2 stub) ────────────────────────────────────────────────

def post_tweet_thread(tweets: list[str], shipping_event_id: int) -> list[str]:
    """Stub — saves tweets to DB but does not post. Returns empty URL list."""
    db = get_db()
    content_id = save_content(
        db, shipping_event_id, "twitter", "\n---\n".join(tweets),
        status="draft", metadata={"tweets": tweets},
    )
    log_action(db, "save_twitter_draft", content_id, {"note": "Twitter API not configured"})
    db.close()
    return []


# ── Newsletter (Phase 2 stub) ─────────────────────────────────────────────

def queue_newsletter(subject: str, body: str, shipping_event_id: int) -> int:
    """Save newsletter to DB as queued. Returns content ID."""
    db = get_db()
    content_id = save_content(
        db, shipping_event_id, "newsletter", body,
        title=subject, status="queued",
    )
    log_action(db, "queue_newsletter", content_id)
    db.close()
    return content_id
