"""Core orchestrator — uses the system `claude` CLI for content generation."""

import json
import logging
import os
import subprocess
import tempfile
from datetime import datetime, timezone

from marketing.config import ROOT_DIR
from marketing.db import get_db, mark_event_processed, save_content, log_action
from marketing.detect import ShippingEvent, check_for_new_shipping
from marketing.generate import build_system_prompt, build_generation_prompt
from marketing.publish import (
    commit_blog_post, commit_blog_post_pt, commit_and_push_blog,
    save_linkedin_draft, _slugify,
)

log = logging.getLogger("marketing")

MVP_CHANNELS = ["blog", "blog_pt", "linkedin"]


def _generate_content(event: ShippingEvent, channel: str) -> str:
    """Call the system claude CLI for content generation. Returns generated text."""
    system_prompt = build_system_prompt(event, channel)
    user_prompt = build_generation_prompt(event, channel)

    combined_prompt = (
        f"INSTRUCTIONS — follow these exactly:\n\n{system_prompt}\n\n"
        f"---\n\nTASK:\n\n{user_prompt}"
    )

    # Write prompt to a temp file to avoid shell argument length limits
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(combined_prompt)
        prompt_file = f.name

    env = {k: v for k, v in os.environ.items()}
    env.pop("CLAUDECODE", None)
    env.pop("ANTHROPIC_API_KEY", None)

    try:
        result = subprocess.run(
            [
                "claude", "-p",
                f"Read the file {prompt_file} and follow the instructions inside it exactly. Output only the final content, no commentary.",
                "--output-format", "json",
                "--max-turns", "2",
                "--permission-mode", "bypassPermissions",
            ],
            capture_output=True, text=True, timeout=300,
            cwd=str(ROOT_DIR), env=env,
        )
    finally:
        os.unlink(prompt_file)

    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        # Try to extract error from JSON
        try:
            data = json.loads(stdout)
            raise RuntimeError(f"claude error: {data.get('result', stderr or stdout)}")
        except json.JSONDecodeError:
            raise RuntimeError(f"claude failed (exit {result.returncode}): {stderr or stdout}")

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return result.stdout.strip()

    if data.get("is_error"):
        raise RuntimeError(f"claude error: {data.get('result', 'unknown')}")

    return data.get("result", "")


def _extract_title_and_body(content: str, fallback_title: str) -> tuple[str, str, str]:
    """Extract title, subtitle, and body from generated markdown content."""
    lines = content.strip().split("\n")
    title = lines[0].lstrip("# ").strip() if lines else fallback_title
    subtitle = ""
    if len(lines) > 1 and not lines[1].startswith("#") and lines[1].strip():
        subtitle = lines[1].strip()
    body_start = 1 if not subtitle else 2
    body = "\n".join(lines[body_start:]).strip()
    return title, subtitle, body


def _process_channel(event: ShippingEvent, channel: str, event_db_id: int,
                     blog_state: dict | None = None):
    """Generate content for a channel and publish it.

    blog_state is a shared dict for coordinating EN/PT blog posts:
      - After 'blog': stores en_slug, en_title
      - After 'blog_pt': commits both EN+PT together
    """
    log.info(f"Generating {channel} content for {event.repo} {event.ref}")

    try:
        content = _generate_content(event, channel)
        if not content.strip():
            log.warning(f"Empty content generated for {channel}")
            return

        log.info(f"Generated {len(content)} chars for {channel}")

        if channel == "blog":
            title, subtitle, body = _extract_title_and_body(content, f"Decompose {event.ref}")
            body_html = _markdown_to_html(body)
            excerpt = subtitle or (body[:150].replace("\n", " ") + "...")
            en_slug = _slugify(title)

            url = commit_blog_post(
                title=title, subtitle=subtitle,
                body_html=body_html, excerpt=excerpt,
                description=excerpt[:200],
                shipping_event_id=event_db_id,
                slug=en_slug,
                markdown=content,
            )
            log.info(f"Blog EN written: {url}")

            # Store slug for PT to use
            if blog_state is not None:
                blog_state["en_slug"] = en_slug
                blog_state["en_title"] = title

        elif channel == "blog_pt":
            title_pt, subtitle_pt, body_pt = _extract_title_and_body(content, f"Decompose {event.ref}")
            body_html_pt = _markdown_to_html(body_pt)
            excerpt_pt = subtitle_pt or (body_pt[:150].replace("\n", " ") + "...")
            pt_slug = _slugify(title_pt)
            en_slug = blog_state.get("en_slug", "") if blog_state else ""
            en_title = blog_state.get("en_title", "") if blog_state else ""

            url_pt = commit_blog_post_pt(
                title_pt=title_pt, subtitle_pt=subtitle_pt,
                body_html_pt=body_html_pt, excerpt_pt=excerpt_pt,
                description_pt=excerpt_pt[:200],
                shipping_event_id=event_db_id,
                slug_pt=pt_slug, en_slug=en_slug,
                markdown=content,
            )
            log.info(f"Blog PT written: {url_pt}")

            # Now commit and push both EN + PT together
            commit_and_push_blog(en_slug, pt_slug, en_title or title_pt)
            log.info("Blog committed and pushed (EN + PT)")

        elif channel == "linkedin":
            content_id = save_linkedin_draft(content, event_db_id)
            log.info(f"LinkedIn draft saved (ID: {content_id})")

        else:
            db = get_db()
            save_content(db, event_db_id, channel, content, status="draft")
            db.close()
            log.info(f"{channel} content saved as draft")

        db = get_db()
        log_action(db, f"generate_{channel}", details={
            "repo": event.repo, "ref": event.ref, "length": len(content),
        })
        db.close()

    except Exception as e:
        log.error(f"Error for {channel}: {e}", exc_info=True)
        db = get_db()
        log_action(db, "generate_error", details={"channel": channel, "error": str(e)})
        db.close()


def _markdown_to_html(text: str) -> str:
    """Simple markdown-to-HTML for blog body content."""
    import html as _html
    import re
    lines = text.split("\n")
    html_parts = []
    in_code_block = False
    code_lines = []
    in_list = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_list:
                html_parts.append("            </ul>")
                in_list = False
            if in_code_block:
                html_parts.append(
                    '<div class="code-block">' + _html.escape("\n".join(code_lines)) + "</div>"
                )
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            if in_list:
                html_parts.append("            </ul>")
                in_list = False
            continue
        elif stripped.startswith("## "):
            if in_list:
                html_parts.append("            </ul>")
                in_list = False
            html_parts.append(f"            <h2>{_html.escape(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            if in_list:
                html_parts.append("            </ul>")
                in_list = False
            html_parts.append(f"            <h3>{_html.escape(stripped[4:])}</h3>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_parts.append("            <ul>")
                in_list = True
            html_parts.append(f"                <li>{_html.escape(stripped[2:])}</li>")
        elif stripped.startswith("> "):
            if in_list:
                html_parts.append("            </ul>")
                in_list = False
            html_parts.append(
                f'            <blockquote><p>{_html.escape(stripped[2:])}</p></blockquote>'
            )
        else:
            if in_list:
                html_parts.append("            </ul>")
                in_list = False
            escaped = _html.escape(stripped)
            processed = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
            processed = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", processed)
            html_parts.append(f"            <p>{processed}</p>")

    if in_list:
        html_parts.append("            </ul>")
    if in_code_block and code_lines:
        html_parts.append(
            '<div class="code-block">' + _html.escape("\n".join(code_lines)) + "</div>"
        )

    return "\n\n".join(html_parts)


def run_agent_cycle():
    """One cycle: detect shipping events, generate content for each."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    log.info("Checking for new shipping events...")
    events = check_for_new_shipping()

    if not events:
        log.info("No new shipping events detected")
        return

    log.info(f"Found {len(events)} new shipping event(s)")

    db = get_db()

    for event in events:
        log.info(f"Processing: {event.repo} {event.ref} ({event.event_type})")

        rows = db.execute(
            "SELECT id FROM shipping_events WHERE repo = ? AND ref = ? ORDER BY id DESC LIMIT 1",
            (event.repo, event.ref),
        ).fetchall()
        if not rows:
            log.error(f"Could not find DB record for {event.repo} {event.ref}")
            continue
        event_db_id = rows[0]["id"]

        blog_state = {}
        for channel in MVP_CHANNELS:
            _process_channel(event, channel, event_db_id, blog_state=blog_state)

        mark_event_processed(db, event_db_id)
        log_action(db, "event_processed", details={
            "repo": event.repo, "ref": event.ref, "channels": MVP_CHANNELS,
        })
        log.info(f"Completed: {event.repo} {event.ref}")

    db.close()
    log.info("Agent cycle complete")
