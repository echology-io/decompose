"""Core orchestrator — Claude Agent SDK loop for content generation."""

import json
import logging
from datetime import datetime, timezone

from claude_agent_sdk import query, ClaudeAgentOptions

from marketing.config import ANTHROPIC_API_KEY, DECOMPOSE_MCP_CMD, DECOMPOSE_MCP_ARGS, ROOT_DIR
from marketing.db import get_db, mark_event_processed, log_action
from marketing.detect import ShippingEvent, check_for_new_shipping
from marketing.generate import build_system_prompt, build_generation_prompt
from marketing.tools import get_marketing_tools_server

log = logging.getLogger("marketing")

# Channels to generate content for on each shipping event
MVP_CHANNELS = ["blog", "linkedin"]


async def _generate_for_channel(event: ShippingEvent, channel: str, event_db_id: int):
    """Run the Claude Agent SDK to generate and publish content for one channel."""
    system_prompt = build_system_prompt(event, channel)
    user_prompt = build_generation_prompt(event, channel)

    # Add the shipping event DB ID to the prompt so tools can reference it
    user_prompt += f"\n\nIMPORTANT: The shipping_event_id for tool calls is {event_db_id}."

    tools_server = get_marketing_tools_server()

    # Determine which tools the agent can use based on channel
    allowed_tools = ["mcp__marketing__save_content"]
    if channel == "blog":
        allowed_tools.append("mcp__marketing__publish_blog")
    elif channel == "linkedin":
        allowed_tools.append("mcp__marketing__save_linkedin_draft")
    elif channel == "twitter":
        allowed_tools.append("mcp__marketing__save_twitter_draft")
    elif channel == "newsletter":
        allowed_tools.append("mcp__marketing__queue_newsletter")

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=allowed_tools,
        mcp_servers={
            "marketing": tools_server,
            "decompose": {
                "command": DECOMPOSE_MCP_CMD,
                "args": DECOMPOSE_MCP_ARGS,
            },
        },
        permission_mode="bypassPermissions",
        cwd=str(ROOT_DIR),
        model="claude-sonnet-4-5-20250929",
        max_turns=10,
    )

    db = get_db()
    log.info(f"Generating {channel} content for {event.repo} {event.ref}")

    try:
        async for message in query(prompt=user_prompt, options=options):
            # Log assistant messages for audit trail
            if hasattr(message, "content"):
                for block in getattr(message, "content", []):
                    if hasattr(block, "text"):
                        log.debug(f"[{channel}] {block.text[:200]}")
    except Exception as e:
        log.error(f"Agent error for {channel}: {e}")
        log_action(db, "generate_error", details={"channel": channel, "error": str(e)})
    finally:
        db.close()


async def run_agent_cycle():
    """One cycle: detect shipping events, generate content for each."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    if not ANTHROPIC_API_KEY:
        log.error("ANTHROPIC_API_KEY not set — cannot run agent")
        return

    log.info("Checking for new shipping events...")
    events = check_for_new_shipping()

    if not events:
        log.info("No new shipping events detected")
        return

    log.info(f"Found {len(events)} new shipping event(s)")

    db = get_db()

    for event in events:
        log.info(f"Processing: {event.repo} {event.ref} ({event.event_type})")

        # Find the DB row for this event
        rows = db.execute(
            "SELECT id FROM shipping_events WHERE repo = ? AND ref = ? ORDER BY id DESC LIMIT 1",
            (event.repo, event.ref),
        ).fetchall()
        if not rows:
            log.error(f"Could not find DB record for {event.repo} {event.ref}")
            continue
        event_db_id = rows[0]["id"]

        # Generate content for each channel
        for channel in MVP_CHANNELS:
            await _generate_for_channel(event, channel, event_db_id)

        # Mark event as processed
        mark_event_processed(db, event_db_id)
        log_action(db, "event_processed", details={
            "repo": event.repo, "ref": event.ref, "channels": MVP_CHANNELS,
        })
        log.info(f"Completed: {event.repo} {event.ref}")

    db.close()
    log.info("Agent cycle complete")
