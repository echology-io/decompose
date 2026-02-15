"""MCP server — expose decompose as tools for any MCP-compatible agent."""

from __future__ import annotations

import ipaddress
import json
import socket
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from decompose.core import decompose_text

_BLOCKED_NETS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def _validate_url(url: str) -> None:
    """Reject URLs targeting internal/private networks or non-HTTP schemes."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL has no hostname")
    try:
        addrs = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror as e:
        raise ValueError(f"Cannot resolve hostname: {e}") from None
    for _, _, _, _, sockaddr in addrs:
        ip = ipaddress.ip_address(sockaddr[0])
        for net in _BLOCKED_NETS:
            if ip in net:
                raise ValueError(f"URL resolves to blocked address: {ip}")

server = Server("decompose")


class _HTMLToText(HTMLParser):
    """Minimal HTML-to-text converter. No dependencies."""

    def __init__(self):
        super().__init__()
        self._parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        self._skip = tag in ("script", "style", "nav", "footer", "header")
        if tag in ("p", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr"):
            self._parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "footer", "header"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self._parts.append(data)

    def get_text(self) -> str:
        return "".join(self._parts).strip()


def _fetch_url(url: str, timeout: int = 15) -> str:
    """Fetch URL content, convert HTML to plain text. Stdlib only."""
    _validate_url(url)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "decompose/0.1", "Accept": "text/markdown, text/plain, text/html"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        content_type = resp.headers.get("Content-Type", "")
        body = resp.read().decode("utf-8", errors="replace")

        if "text/markdown" in content_type or "text/plain" in content_type:
            return body

        # HTML → plain text
        parser = _HTMLToText()
        parser.feed(body)
        return parser.get_text()


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="decompose_text",
            description=(
                "Decompose text into classified semantic units with authority levels, "
                "risk scores, entity extraction, and irreducibility flags. "
                "No LLM required. Deterministic. Returns structured JSON."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to decompose"},
                    "compact": {"type": "boolean", "description": "Omit zero-value fields", "default": False},
                    "chunk_size": {"type": "integer", "description": "Max chars per unit", "default": 2000},
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="decompose_url",
            description=(
                "Fetch a URL and decompose its content into semantic units. "
                "Handles HTML, Markdown, and plain text."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "format": "uri", "description": "URL to fetch and decompose"},
                    "compact": {"type": "boolean", "description": "Omit zero-value fields", "default": False},
                },
                "required": ["url"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "decompose_text":
        result = decompose_text(
            arguments["text"],
            compact=arguments.get("compact", False),
            chunk_size=arguments.get("chunk_size", 2000),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "decompose_url":
        url = arguments["url"]
        try:
            text = _fetch_url(url)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            return [TextContent(type="text", text=json.dumps({"error": f"Failed to fetch URL: {e}"}))]

        result = decompose_text(text, compact=arguments.get("compact", False))
        result["meta"]["source_url"] = url
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def serve():
    """Run the MCP server on stdio."""
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())
