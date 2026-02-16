#!/usr/bin/env python3
"""
aecai_outreach.py — AI-Powered Outreach Drafting
=================================================
Reads leads from data/leads.jsonl, uses Ollama (llama3) to generate
personalized outreach aligned with the AECai Outbound Sales SOP.

Usage:
    python3 aecai_outreach.py                  # Interactive mode
    python3 aecai_outreach.py list              # Show all leads
    python3 aecai_outreach.py draft <lead_id>   # Draft for specific lead
    python3 aecai_outreach.py draft --all       # Draft for all leads
    python3 aecai_outreach.py batch linkedin     # Batch LinkedIn DMs
    python3 aecai_outreach.py batch email        # Batch cold emails

Requires: Ollama running locally (ollama serve)
Model: llama3 (pull with: ollama pull llama3)
"""

import argparse
import json
import textwrap
from datetime import datetime

from config import cfg

# ── Configuration ──
AECAI_DIR = cfg.BASE_DIR
LEADS_FILE = AECAI_DIR / "data" / "leads.jsonl"
DRAFTS_DIR = AECAI_DIR / "data" / "drafts"
OLLAMA_URL = cfg.OLLAMA_HOST
MODEL = cfg.OLLAMA_MODEL

# ── SOP Templates (from AECai Outbound Sales SOP) ──
FOUNDER_CONTEXT = """
Kyle Vines, founder of AECai. 13 years in civil and geotechnical engineering.
Worked at firms from ENR #60 to ENR #123. Bought an engineering firm, went through 
bankruptcy learning hard lessons about organizational structure. Built an AI system 
inside an ENR Top 200 firm that validated $1.85M in annual operational value across 
200 engineers. Now runs AECai — AI consulting exclusively for engineering firms.

AECai is NOT a software company. It's a consulting practice that happens to build tools.
Everything runs on client hardware. Air-gapped. No cloud. No third-party APIs. Ever.

The offer: $800 AI Discovery & Readiness Assessment (2-week delivery, 100% credit 
toward full engagement at $15K-$75K). Below procurement threshold = credit card sale.
"""

LINKEDIN_DM_TEMPLATE = """
Write a LinkedIn direct message from Kyle Vines (AECai founder) to {name} at {firm}.

CONTEXT ABOUT THE LEAD:
{lead_context}

RULES:
- First person, casual but professional — engineer to engineer
- Under 150 words
- Reference something specific about their firm if possible
- Include the $1.85M proof point naturally (not as a brag)
- End with a soft question, not a hard ask
- Never say "revolutionary", "game-changing", "excited to announce"
- Never use emojis
- Tone: peer conversation, not sales pitch
- If they're at an ENR firm, mention you've worked at similar firms

{founder_context}

Write only the message. No subject line. No explanation.
"""

COLD_EMAIL_TEMPLATE = """
Write a cold email from Kyle Vines (AECai founder) to {name} at {firm}.

CONTEXT ABOUT THE LEAD:
{lead_context}

RULES:
- Subject line: lowercase, max 6 words, conversational
- Plain text only — no HTML, no images, no bold
- Max 150 words in body
- Open with something specific to their firm or role
- Include the engineering credibility (13 years, worked at ENR firms)
- One clear proof point ($1.85M value, or the "page 247" story, or the "Dave retired" story)
- End with a question, not a CTA
- Sign off: Kyle Vines / AECai / aecai.io

{founder_context}

Format as:
Subject: [subject line]

[body]

[signature]
"""

FOLLOWUP_TEMPLATE = """
Write a follow-up message from Kyle Vines to {name} at {firm}.
This is follow-up #{followup_num}. Previous outreach was {days_ago} days ago via {channel}.

RULES:
- Shorter than the original (under 80 words)
- Add ONE new angle or data point they haven't seen
- If follow-up #2+, more direct but not pushy
- If follow-up #3, this is the break-up email — graceful, leave the door open
- Never apologize for following up

New angles to choose from:
- "Your best engineer is everyone's search engine — 3-5 interruptions per day"
- "Spec review: page 247 had a compaction change that contradicted the geotech report"
- "When a 30-year engineer walks out, the knowledge is technically in your files — nobody knows how to find it"
- "68% of rework comes from missed requirements buried in specs"

{founder_context}

Write only the message.
"""


def load_leads():
    """Load all leads from JSONL file."""
    if not LEADS_FILE.exists():
        return []
    leads = []
    for line in LEADS_FILE.read_text().strip().split("\n"):
        if line.strip():
            try:
                leads.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return leads


def call_ollama(prompt, model=MODEL):
    """Call Ollama API for text generation."""
    import urllib.request

    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 500,
            },
        }
    ).encode()

    try:
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data.get("response", "").strip()
    except Exception as e:
        return f"[Ollama error: {e}. Is 'ollama serve' running?]"


def check_ollama():
    """Check if Ollama is running and model is available."""
    import urllib.request

    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5) as resp:
            data = json.loads(resp.read())
            models = [m["name"] for m in data.get("models", [])]
            if any(MODEL in m for m in models):
                return True, f"Ollama running, {MODEL} available"
            else:
                return False, f"Ollama running but {MODEL} not found. Run: ollama pull {MODEL}"
    except Exception:
        return False, "Ollama not running. Start with: ollama serve &"


def build_lead_context(lead):
    """Build context string from lead data."""
    parts = []
    if lead.get("name"):
        parts.append(f"Name: {lead['name']}")
    if lead.get("email"):
        parts.append(f"Email: {lead['email']}")
    if lead.get("firm"):
        parts.append(f"Firm: {lead['firm']}")
    if lead.get("role") or lead.get("title"):
        parts.append(f"Role: {lead.get('role') or lead.get('title')}")
    if lead.get("source"):
        parts.append(f"Source: {lead['source']} (how they found us)")
    if lead.get("pain_point") or lead.get("custom"):
        parts.append(f"Pain point: {lead.get('pain_point') or lead.get('custom')}")
    if lead.get("team_size"):
        parts.append(f"Team size: {lead['team_size']}")
    if lead.get("timestamp"):
        parts.append(f"First contact: {lead['timestamp'][:10]}")
    return "\n".join(parts) if parts else "Minimal data available — use a general approach."


def draft_message(lead, msg_type="linkedin", followup_num=0, days_ago=0, channel="linkedin"):
    """Generate a draft message for a lead."""
    lead_context = build_lead_context(lead)
    name = lead.get("name", "there")
    firm = lead.get("firm", "your firm")

    if msg_type == "linkedin":
        prompt = LINKEDIN_DM_TEMPLATE.format(
            name=name, firm=firm, lead_context=lead_context, founder_context=FOUNDER_CONTEXT
        )
    elif msg_type == "email":
        prompt = COLD_EMAIL_TEMPLATE.format(
            name=name, firm=firm, lead_context=lead_context, founder_context=FOUNDER_CONTEXT
        )
    elif msg_type == "followup":
        prompt = FOLLOWUP_TEMPLATE.format(
            name=name,
            firm=firm,
            followup_num=followup_num,
            days_ago=days_ago,
            channel=channel,
            founder_context=FOUNDER_CONTEXT,
        )
    else:
        prompt = LINKEDIN_DM_TEMPLATE.format(
            name=name, firm=firm, lead_context=lead_context, founder_context=FOUNDER_CONTEXT
        )

    return call_ollama(prompt)


def save_draft(lead, msg_type, content):
    """Save a draft to the drafts directory."""
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = lead.get("name", "unknown").replace(" ", "_").lower()
    filename = f"{stamp}_{name}_{msg_type}.txt"
    filepath = DRAFTS_DIR / filename

    header = f"""# AECai Outreach Draft
# Type: {msg_type}
# Lead: {lead.get("name", "?")} at {lead.get("firm", "?")}
# Email: {lead.get("email", "?")}
# Generated: {datetime.now().isoformat()}
# ---

"""
    filepath.write_text(header + content)
    return filepath


# ═══════════════════════════════════════════════════════════
#  INTERACTIVE MODE
# ═══════════════════════════════════════════════════════════


def interactive():
    """Interactive outreach drafting session."""
    print("\n╔═══════════════════════════════════════════════╗")
    print("║   AECai Outreach — AI-Powered Draft Engine    ║")
    print("╚═══════════════════════════════════════════════╝\n")

    # Check Ollama
    ok, msg = check_ollama()
    if ok:
        print(f"  ✓ {msg}")
    else:
        print(f"  ✗ {msg}")
        return

    # Load leads
    leads = load_leads()
    print(f"  ✓ {len(leads)} leads loaded from {LEADS_FILE}\n")

    if not leads:
        print("  No leads found. Add leads via the website or manually to data/leads.jsonl")
        return

    while True:
        print("─" * 50)
        print("\nCommands:")
        print("  [l]ist        — Show all leads")
        print("  [d]raft <#>   — Draft for lead # (linkedin)")
        print("  [e]mail <#>   — Draft cold email for lead #")
        print("  [f]ollowup <#> — Draft follow-up for lead #")
        print("  [c]ustom      — Draft for a new contact (not in leads)")
        print("  [q]uit\n")

        cmd = input("→ ").strip().lower()

        if cmd in ("q", "quit", "exit"):
            print("\nDrafts saved to: ~/aecai/data/drafts/")
            break

        elif cmd in ("l", "list"):
            print(f"\n{'#':<4} {'Name':<25} {'Firm':<25} {'Email':<30} {'Source':<12}")
            print("─" * 96)
            for i, lead in enumerate(leads):
                print(
                    f"{i:<4} {lead.get('name', '?')[:24]:<25} {lead.get('firm', '?')[:24]:<25} {lead.get('email', '?')[:29]:<30} {lead.get('source', '?')[:11]:<12}"
                )
            print()

        elif cmd.startswith(("d ", "draft ")):
            try:
                idx = int(cmd.split()[-1])
                lead = leads[idx]
                print(f"\n  Drafting LinkedIn DM for {lead.get('name')} at {lead.get('firm')}...")
                content = draft_message(lead, "linkedin")
                filepath = save_draft(lead, "linkedin", content)
                print(f"\n{'─' * 50}")
                print(content)
                print(f"{'─' * 50}")
                print(f"  Saved: {filepath}\n")
            except (ValueError, IndexError):
                print("  Invalid lead number. Use 'list' to see leads.\n")

        elif cmd.startswith(("e ", "email ")):
            try:
                idx = int(cmd.split()[-1])
                lead = leads[idx]
                print(f"\n  Drafting cold email for {lead.get('name')} at {lead.get('firm')}...")
                content = draft_message(lead, "email")
                filepath = save_draft(lead, "email", content)
                print(f"\n{'─' * 50}")
                print(content)
                print(f"{'─' * 50}")
                print(f"  Saved: {filepath}\n")
            except (ValueError, IndexError):
                print("  Invalid lead number. Use 'list' to see leads.\n")

        elif cmd.startswith(("f ", "followup ")):
            try:
                idx = int(cmd.split()[-1])
                lead = leads[idx]
                num = input("  Follow-up # (1, 2, or 3): ").strip()
                days = input("  Days since last contact: ").strip()
                ch = input("  Last channel (linkedin/email): ").strip() or "linkedin"
                print(f"\n  Drafting follow-up #{num}...")
                content = draft_message(
                    lead, "followup", followup_num=int(num) if num else 1, days_ago=int(days) if days else 7, channel=ch
                )
                filepath = save_draft(lead, f"followup_{num}", content)
                print(f"\n{'─' * 50}")
                print(content)
                print(f"{'─' * 50}")
                print(f"  Saved: {filepath}\n")
            except (ValueError, IndexError):
                print("  Invalid lead number.\n")

        elif cmd in ("c", "custom"):
            name = input("  Name: ").strip()
            email = input("  Email: ").strip()
            firm = input("  Firm: ").strip()
            role = input("  Role/Title: ").strip()
            pain = input("  Pain point (optional): ").strip()

            lead = {"name": name, "email": email, "firm": firm, "role": role, "custom": pain, "id": "custom"}

            msg_type = input("  Type [linkedin/email]: ").strip() or "linkedin"
            print(f"\n  Drafting {msg_type}...")
            content = draft_message(lead, msg_type)
            filepath = save_draft(lead, msg_type, content)
            print(f"\n{'─' * 50}")
            print(content)
            print(f"{'─' * 50}")
            print(f"  Saved: {filepath}\n")

        else:
            print("  Unknown command. Try: list, draft 0, email 0, followup 0, custom, quit\n")


# ═══════════════════════════════════════════════════════════
#  BATCH MODE
# ═══════════════════════════════════════════════════════════


def batch_draft(msg_type="linkedin", limit=None):
    """Generate drafts for all leads."""
    ok, msg = check_ollama()
    if not ok:
        print(f"  ✗ {msg}")
        return

    leads = load_leads()
    if not leads:
        print("  No leads found.")
        return

    if limit:
        leads = leads[:limit]

    print(f"\n  Generating {msg_type} drafts for {len(leads)} leads...\n")

    for i, lead in enumerate(leads):
        name = lead.get("name", "?")
        firm = lead.get("firm", "?")
        print(f"  [{i + 1}/{len(leads)}] {name} at {firm}...", end=" ", flush=True)
        content = draft_message(lead, msg_type)
        filepath = save_draft(lead, msg_type, content)
        print(f"✓ → {filepath.name}")

    print(f"\n  ✅ {len(leads)} drafts saved to {DRAFTS_DIR}/")


# ═══════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(
        description="AECai AI-Powered Outreach Drafting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python3 aecai_outreach.py              Interactive mode
          python3 aecai_outreach.py list          Show all leads
          python3 aecai_outreach.py draft 0       Draft LinkedIn DM for lead #0
          python3 aecai_outreach.py batch linkedin Generate all LinkedIn drafts
          python3 aecai_outreach.py batch email    Generate all email drafts
        """),
    )
    parser.add_argument("command", nargs="?", default="interactive", help="Command: interactive, list, draft, batch")
    parser.add_argument("target", nargs="?", default=None, help="Lead index or message type")
    parser.add_argument("--limit", type=int, default=None, help="Limit batch processing to N leads")

    args = parser.parse_args()

    if args.command == "interactive":
        interactive()

    elif args.command == "list":
        leads = load_leads()
        print(f"\n  {len(leads)} leads in {LEADS_FILE}\n")
        print(f"  {'#':<4} {'Name':<25} {'Firm':<25} {'Email':<30}")
        print("  " + "─" * 84)
        for i, lead in enumerate(leads):
            print(
                f"  {i:<4} {lead.get('name', '?')[:24]:<25} {lead.get('firm', '?')[:24]:<25} {lead.get('email', '?')[:29]:<30}"
            )

    elif args.command == "draft":
        if args.target is None:
            print("  Usage: aecai_outreach.py draft <lead_number>")
            print("         aecai_outreach.py draft --all")
            return
        ok, msg = check_ollama()
        if not ok:
            print(f"  ✗ {msg}")
            return
        if args.target == "--all":
            batch_draft("linkedin", limit=args.limit)
        else:
            leads = load_leads()
            try:
                idx = int(args.target)
                lead = leads[idx]
                print(f"\n  Drafting LinkedIn DM for {lead.get('name')} at {lead.get('firm')}...")
                content = draft_message(lead, "linkedin")
                filepath = save_draft(lead, "linkedin", content)
                print(f"\n{content}\n")
                print(f"  Saved: {filepath}")
            except (ValueError, IndexError):
                print(f"  Invalid lead number. Use 'list' to see {len(leads)} leads.")

    elif args.command == "batch":
        msg_type = args.target or "linkedin"
        if msg_type not in ("linkedin", "email", "followup"):
            print(f"  Invalid type: {msg_type}. Use: linkedin, email, followup")
            return
        batch_draft(msg_type, limit=args.limit)

    else:
        interactive()


if __name__ == "__main__":
    main()
