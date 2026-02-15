"""CLI — decompose from the command line. Stdin or --text, stdout JSON."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys

from decompose.core import decompose_text


def main():
    parser = argparse.ArgumentParser(
        prog="decompose",
        description="Stop prompting. Start decomposing. Structured intelligence from any text.",
    )
    parser.add_argument("--text", "-t", help="Text to decompose (or pipe via stdin)")
    parser.add_argument("--compact", "-c", action="store_true", help="Compact output (omit zero-value fields)")
    parser.add_argument("--chunk-size", type=int, default=2000, help="Max characters per unit (default: 2000)")
    parser.add_argument("--pretty", "-p", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--serve", action="store_true", help="Run as MCP server (stdio)")
    parser.add_argument("--version", "-v", action="store_true", help="Print version")

    args = parser.parse_args()

    if args.version:
        from decompose import __version__
        print(f"decompose {__version__}")
        return

    if args.serve:
        from decompose.mcp_server import serve
        asyncio.run(serve())
        return

    # Get text from --text flag or stdin
    if args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    result = decompose_text(text, compact=args.compact, chunk_size=args.chunk_size)

    indent = 2 if args.pretty else None
    json.dump(result, sys.stdout, indent=indent)
    if sys.stdout.isatty():
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
