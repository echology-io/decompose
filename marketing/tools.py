"""Custom tool definitions for the Claude Agent SDK."""

import json
from typing import Any

from claude_agent_sdk import tool, create_sdk_mcp_server

from marketing.db import get_db, save_content, update_content_status, log_action
from marketing.publish import (
    commit_blog_post,
    save_linkedin_draft,
    post_tweet_thread,
    queue_newsletter,
)


@tool("publish_blog", "Write and publish a blog post to echology.io/blog. Commits HTML, updates index, pushes to GitHub. Auto-deploys via GitHub Pages.", {
    "title": str,
    "subtitle": str,
    "body_html": str,
    "excerpt": str,
    "description": str,
    "shipping_event_id": int,
    "slug": str,
    "h1_line1": str,
    "h1_line2": str,
})
async def publish_blog_tool(args: dict[str, Any]) -> dict[str, Any]:
    url = commit_blog_post(
        title=args["title"],
        subtitle=args["subtitle"],
        body_html=args["body_html"],
        excerpt=args["excerpt"],
        description=args["description"],
        shipping_event_id=args["shipping_event_id"],
        slug=args.get("slug"),
        h1_line1=args.get("h1_line1"),
        h1_line2=args.get("h1_line2"),
    )
    return {"content": [{"type": "text", "text": f"Blog post published: {url}"}]}


@tool("save_linkedin_draft", "Save a LinkedIn post draft for manual posting.", {
    "content": str,
    "shipping_event_id": int,
})
async def save_linkedin_draft_tool(args: dict[str, Any]) -> dict[str, Any]:
    content_id = save_linkedin_draft(args["content"], args["shipping_event_id"])
    return {"content": [{"type": "text", "text": f"LinkedIn draft saved (content ID: {content_id})"}]}


@tool("save_twitter_draft", "Save a Twitter thread draft (Twitter API not yet configured).", {
    "tweets": list,
    "shipping_event_id": int,
})
async def save_twitter_draft_tool(args: dict[str, Any]) -> dict[str, Any]:
    urls = post_tweet_thread(args["tweets"], args["shipping_event_id"])
    return {"content": [{"type": "text", "text": "Twitter draft saved to database (posting not yet configured)"}]}


@tool("queue_newsletter", "Queue a newsletter edition for later sending.", {
    "subject": str,
    "body": str,
    "shipping_event_id": int,
})
async def queue_newsletter_tool(args: dict[str, Any]) -> dict[str, Any]:
    content_id = queue_newsletter(args["subject"], args["body"], args["shipping_event_id"])
    return {"content": [{"type": "text", "text": f"Newsletter queued (content ID: {content_id})"}]}


@tool("save_content", "Save generated content to the database with a given channel and status.", {
    "shipping_event_id": int,
    "channel": str,
    "body": str,
    "title": str,
    "status": str,
})
async def save_content_tool(args: dict[str, Any]) -> dict[str, Any]:
    db = get_db()
    content_id = save_content(
        db,
        shipping_event_id=args["shipping_event_id"],
        channel=args["channel"],
        body=args["body"],
        title=args.get("title", ""),
        status=args.get("status", "draft"),
    )
    db.close()
    return {"content": [{"type": "text", "text": f"Content saved (ID: {content_id})"}]}


def get_marketing_tools_server():
    """Create the in-process MCP server with all marketing tools."""
    return create_sdk_mcp_server(
        name="marketing",
        version="1.0.0",
        tools=[
            publish_blog_tool,
            save_linkedin_draft_tool,
            save_twitter_draft_tool,
            queue_newsletter_tool,
            save_content_tool,
        ],
    )
