"""Channel publishers — blog commit, LinkedIn draft, Twitter stub, newsletter stub."""

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from marketing.config import BLOG_DIR, BLOG_INDEX, ROOT_DIR, DOCS_DIR
from marketing.db import get_db, save_content, update_content_status, log_action

# ── Paths ──────────────────────────────────────────────────────────────────
PT_BLOG_DIR = ROOT_DIR / "docs" / "pt" / "blog"
PT_BLOG_INDEX = ROOT_DIR / "docs" / "pt" / "blog.html"

# ── Portuguese date formatting ─────────────────────────────────────────────
_PT_MONTHS = {
    1: "janeiro", 2: "fevereiro", 3: "marco", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
}


def _pt_date_display(dt: datetime) -> str:
    return f"{dt.day} de {_PT_MONTHS[dt.month]} de {dt.year}"


# ── Shared HTML template (parameterized for EN/PT) ─────────────────────────

_BLOG_TEMPLATE = """\
<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Echology</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title} — Echology">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://echology.io/{url_prefix}blog/{slug}">
    <meta property="article:published_time" content="{date}">
    <meta name="twitter:card" content="summary">
    <link rel="stylesheet" href="{css_path}">
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
            <a href="{home_path}" class="logo">echology<span>.</span></a>
            <button class="nav-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')">&#9776;</button>
            <div class="nav-links">
                <a href="{nav_about}">{label_about}</a>
                <a href="{nav_aecai}">AECai</a>
                <a href="{nav_decompose}">Decompose</a>
                <a href="{nav_blog}" class="active">Blog</a>
                <a href="{nav_contact}">{label_contact}</a>
                <a href="{lang_toggle_url}" class="lang-toggle" title="{lang_toggle_title}">{lang_toggle_flag}</a>
            </div>
        </div>
    </nav>

    <section class="hero">
        <div class="container container--narrow">
            <h1>{h1_line1}<br><span>{h1_line2}</span></h1>
            <p class="sub">{subtitle}</p>
            <div class="post-meta">
                <div class="date">{date_display}</div>
                <div class="reading">{reading_time} {reading_label}</div>
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
                <a href="{nav_about}">{label_about}</a>
                <a href="{nav_contact}">{label_contact}</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""

_BLOG_INDEX_ENTRY_EN = """\
                <a href="/blog/{slug}" class="post-item">
                    <div class="post-date">{date_display}</div>
                    <div class="post-title">{title}</div>
                    <div class="post-excerpt">{excerpt}</div>
                </a>"""

_BLOG_INDEX_ENTRY_PT = """\
                <a href="/pt/blog/{slug}" class="post-item">
                    <div class="post-date">{date_display}</div>
                    <div class="post-title">{title}</div>
                    <div class="post-excerpt">{excerpt}</div>
                </a>"""


def _estimate_reading_time(text: str) -> int:
    words = len(text.split())
    return max(1, round(words / 250))


def _slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s-]+", "-", slug).strip("-")
    return slug


def _render_blog_html(
    title: str, subtitle: str, body_html: str, description: str,
    slug: str, h1_line1: str, h1_line2: str,
    date_str: str, date_display: str, reading_time: int,
    lang: str = "en",
    en_slug: str = "",
    pt_slug: str = "",
) -> str:
    """Render a blog post HTML page for either EN or PT."""
    is_pt = lang == "pt-BR"
    return _BLOG_TEMPLATE.format(
        lang=lang,
        title=title,
        description=description,
        url_prefix="pt/" if is_pt else "",
        slug=slug,
        date=date_str,
        css_path="../../style.css" if is_pt else "../style.css",
        home_path="/pt/" if is_pt else "/",
        nav_about="/pt/sobre" if is_pt else "/about",
        nav_aecai="/pt/aecai" if is_pt else "/aecai",
        nav_decompose="/pt/decompose" if is_pt else "/decompose",
        nav_blog="/pt/blog" if is_pt else "/blog",
        nav_contact="/pt/contato" if is_pt else "/contact",
        label_about="Sobre" if is_pt else "About",
        label_contact="Contato" if is_pt else "Contact",
        lang_toggle_url=f"/blog/{en_slug}" if is_pt else f"/pt/blog/{pt_slug}",
        lang_toggle_title="English" if is_pt else "Portugues",
        lang_toggle_flag="&#127482;&#127480;" if is_pt else "&#127463;&#127479;",
        h1_line1=h1_line1,
        h1_line2=h1_line2,
        subtitle=subtitle,
        date_display=date_display,
        reading_time=reading_time,
        reading_label="min de leitura" if is_pt else "min read",
        body_html=body_html,
    )


# ── Blog (English) ────────────────────────────────────────────────────────

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
    pt_slug: str = "",
) -> str:
    """Write EN blog HTML, update EN index. Does NOT commit/push (done after PT)."""
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

    html = _render_blog_html(
        title=title, subtitle=subtitle, body_html=body_html,
        description=description, slug=slug,
        h1_line1=h1_line1, h1_line2=h1_line2,
        date_str=date_str, date_display=date_display,
        reading_time=reading_time, lang="en",
        pt_slug=pt_slug,
    )

    post_path = BLOG_DIR / f"{slug}.html"
    post_path.write_text(html)

    # Update EN blog index
    index_html = BLOG_INDEX.read_text()
    new_entry = _BLOG_INDEX_ENTRY_EN.format(
        slug=slug, date_display=date_display, title=title, excerpt=excerpt,
    )
    index_html = index_html.replace(
        '<div class="post-list">',
        f'<div class="post-list">\n{new_entry}',
    )
    BLOG_INDEX.write_text(index_html)

    blog_url = f"https://echology.io/blog/{slug}"

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


# ── Blog (Portuguese) ─────────────────────────────────────────────────────

def commit_blog_post_pt(
    title_pt: str,
    subtitle_pt: str,
    body_html_pt: str,
    excerpt_pt: str,
    description_pt: str,
    shipping_event_id: int,
    slug_pt: str,
    en_slug: str,
    h1_line1: str | None = None,
    h1_line2: str | None = None,
) -> str:
    """Write PT blog HTML, update PT index. Does NOT commit/push (done by agent)."""
    if not h1_line1:
        words = title_pt.split()
        mid = len(words) // 2
        h1_line1 = " ".join(words[:mid]) if mid > 0 else title_pt
        h1_line2 = " ".join(words[mid:]) if mid > 0 else ""
    if not h1_line2:
        h1_line2 = ""

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    date_display = _pt_date_display(now)
    reading_time = _estimate_reading_time(body_html_pt)

    html = _render_blog_html(
        title=title_pt, subtitle=subtitle_pt, body_html=body_html_pt,
        description=description_pt, slug=slug_pt,
        h1_line1=h1_line1, h1_line2=h1_line2,
        date_str=date_str, date_display=date_display,
        reading_time=reading_time, lang="pt-BR",
        en_slug=en_slug,
    )

    post_path = PT_BLOG_DIR / f"{slug_pt}.html"
    post_path.write_text(html)

    # Update PT blog index
    index_html = PT_BLOG_INDEX.read_text()
    new_entry = _BLOG_INDEX_ENTRY_PT.format(
        slug=slug_pt, date_display=date_display,
        title=title_pt, excerpt=excerpt_pt,
    )
    index_html = index_html.replace(
        '<div class="post-list">',
        f'<div class="post-list">\n{new_entry}',
    )
    PT_BLOG_INDEX.write_text(index_html)

    blog_url = f"https://echology.io/pt/blog/{slug_pt}"

    db = get_db()
    content_id = save_content(
        db, shipping_event_id, "blog_pt", body_html_pt,
        title=title_pt, status="published",
        metadata={"slug": slug_pt, "url": blog_url},
    )
    update_content_status(db, content_id, "published", published_url=blog_url)
    log_action(db, "publish_blog_pt", content_id, {"slug": slug_pt, "url": blog_url})
    db.close()

    return blog_url


# ── Git commit (called after both EN + PT are written) ─────────────────────

def commit_and_push_blog(en_slug: str, pt_slug: str, title: str):
    """Commit all blog changes (EN + PT) and push."""
    files = [
        str(BLOG_DIR / f"{en_slug}.html"),
        str(BLOG_INDEX),
        str(PT_BLOG_DIR / f"{pt_slug}.html"),
        str(PT_BLOG_INDEX),
    ]
    subprocess.run(["git", "add"] + files, cwd=str(ROOT_DIR), capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"blog: {title} (EN + PT)"],
        cwd=str(ROOT_DIR), capture_output=True,
    )
    subprocess.run(["git", "push"], cwd=str(ROOT_DIR), capture_output=True)


# ── LinkedIn (drafts only) ─────────────────────────────────────────────────

def save_linkedin_draft(content: str, shipping_event_id: int) -> int:
    db = get_db()
    content_id = save_content(db, shipping_event_id, "linkedin", content, status="draft")
    log_action(db, "save_linkedin_draft", content_id)
    db.close()
    return content_id


# ── Twitter (Phase 2 stub) ────────────────────────────────────────────────

def post_tweet_thread(tweets: list[str], shipping_event_id: int) -> list[str]:
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
    db = get_db()
    content_id = save_content(
        db, shipping_event_id, "newsletter", body,
        title=subject, status="queued",
    )
    log_action(db, "queue_newsletter", content_id)
    db.close()
    return content_id
