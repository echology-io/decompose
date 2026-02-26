# Changelog

All notable changes to Decompose are documented here.

## [0.2.0] — 2026-02-20

### Added
- AECai pattern backports: improved entity extraction, chunker dict wrapper
- `decompose_url` redirect validation (SSRF mitigation)
- Response size cap (10 MB) on URL fetches
- HTML escaping in marketing agent markdown-to-HTML output

### Changed
- Version bump across pyproject.toml, server.json, `__init__.py`, core.py
- User-Agent string updated to `decompose/0.2`
- RBS demo page updated: Fly.io references removed, API_BASE set to localhost

### Fixed
- SSRF: redirect targets now validated against blocklist
- Marketing agent: unclosed `</ul>` tags in list rendering
- server.json version synced with pyproject.toml (was stuck at 0.1.1)

### Security
- URL fetch opener uses custom `_NoRedirectHandler` to validate redirect chains
- Blocked private/loopback IP ranges in `_validate_url()`

## [0.1.1] — 2026-02-16

### Added
- Security risk classification (`security` category in risk taxonomy)
- `filter_for_llm()` — first-class function to filter decomposed output for LLM context windows
  - Configurable by authority, risk, type, and minimum attention score
  - Returns filtered text, units, and reduction metadata (token estimate, reduction %)
- `decompose_url` MCP tool — fetch and decompose any URL in one call
- Portuguese translation of echology.io

### Changed
- Attention scoring now factors security risk multiplier
- Improved entity extraction for standards and regulatory references

## [0.1.0] — 2026-02-14

### Added
- Initial release on PyPI as `decompose-mcp`
- Core `decompose_text()` function — deterministic text classification
- Authority classification (mandatory, prohibitive, directive, conditional, permissive, informational)
- Risk classification (safety_critical, compliance, financial, contractual, advisory, informational)
- Attention scoring (0.0–10.0 composite of authority weight and risk multiplier)
- Entity extraction (standards, codes, regulations, dates, dollar amounts)
- Irreducibility detection (content that must be preserved verbatim)
- MCP server with `decompose_text` tool
- CLI interface (`decompose` and `decompose-mcp` commands)
- Listed on official MCP Registry, ClawHub
- 63 unit tests, all passing
