"""CLI review dashboard for post-hoc content review."""

import argparse
import sys

from marketing.db import (
    get_db,
    get_all_content,
    get_pending_content,
    get_content_stats,
    update_content_status,
    log_action,
)


def _print_content_row(row: dict):
    """Print a single content row formatted for terminal."""
    status_colors = {
        "draft": "\033[33m",       # yellow
        "published": "\033[32m",   # green
        "needs_review": "\033[31m",  # red
        "rejected": "\033[90m",    # gray
        "queued": "\033[36m",      # cyan
    }
    reset = "\033[0m"
    color = status_colors.get(row["status"], "")

    print(f"\n{'─' * 60}")
    print(f"  ID: {row['id']}  |  Channel: {row['channel']}  |  "
          f"Status: {color}{row['status']}{reset}")
    print(f"  Event: {row.get('repo', '?')} {row.get('ref', '?')}")
    if row.get("title"):
        print(f"  Title: {row['title']}")
    print(f"  Created: {row['created_at']}")
    if row.get("published_url"):
        print(f"  URL: {row['published_url']}")
    # Show first 200 chars of body
    body = row.get("body", "")
    preview = body[:200] + "..." if len(body) > 200 else body
    print(f"  Preview: {preview}")


def cmd_list(args):
    db = get_db()
    rows = get_all_content(db, limit=args.limit)
    db.close()
    if not rows:
        print("No content found.")
        return
    print(f"\n  {len(rows)} content item(s):")
    for row in rows:
        _print_content_row(row)
    print()


def cmd_pending(args):
    db = get_db()
    rows = get_pending_content(db)
    db.close()
    if not rows:
        print("No pending content.")
        return
    print(f"\n  {len(rows)} item(s) awaiting review:")
    for row in rows:
        _print_content_row(row)
    print()


def cmd_approve(args):
    db = get_db()
    update_content_status(db, args.id, "published")
    log_action(db, "manual_approve", args.id)
    db.close()
    print(f"Content #{args.id} approved.")


def cmd_reject(args):
    db = get_db()
    update_content_status(db, args.id, "rejected")
    log_action(db, "manual_reject", args.id, {"reason": args.reason or ""})
    db.close()
    print(f"Content #{args.id} rejected.")


def cmd_show(args):
    db = get_db()
    row = db.execute(
        "SELECT c.*, se.repo, se.ref, se.title as event_title "
        "FROM content c JOIN shipping_events se ON c.shipping_event_id = se.id "
        "WHERE c.id = ?", (args.id,)
    ).fetchone()
    db.close()
    if not row:
        print(f"Content #{args.id} not found.")
        return
    row = dict(row)
    _print_content_row(row)
    print(f"\n  Full content:\n{'─' * 60}")
    print(row.get("body", ""))
    print(f"{'─' * 60}\n")


def cmd_stats(args):
    db = get_db()
    rows = get_content_stats(db)
    db.close()
    if not rows:
        print("No content stats yet.")
        return
    print(f"\n  Content Stats:")
    print(f"  {'Channel':<12} {'Status':<15} {'Count':>5}")
    print(f"  {'─' * 35}")
    for row in rows:
        print(f"  {row['channel']:<12} {row['status']:<15} {row['count']:>5}")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="marketing.review",
        description="Review and manage marketing agent content",
    )
    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="List all content")
    p_list.add_argument("--limit", type=int, default=50)
    p_list.set_defaults(func=cmd_list)

    # pending
    p_pending = sub.add_parser("pending", help="Show items needing review")
    p_pending.set_defaults(func=cmd_pending)

    # approve
    p_approve = sub.add_parser("approve", help="Approve content by ID")
    p_approve.add_argument("id", type=int)
    p_approve.set_defaults(func=cmd_approve)

    # reject
    p_reject = sub.add_parser("reject", help="Reject content by ID")
    p_reject.add_argument("id", type=int)
    p_reject.add_argument("--reason", type=str, default="")
    p_reject.set_defaults(func=cmd_reject)

    # show
    p_show = sub.add_parser("show", help="Show full content by ID")
    p_show.add_argument("id", type=int)
    p_show.set_defaults(func=cmd_show)

    # stats
    p_stats = sub.add_parser("stats", help="Show content statistics")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    if not args.command:
        # Default to list
        args.limit = 50
        cmd_list(args)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
