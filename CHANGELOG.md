# Changelog

All notable changes to Decompose are documented here.

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
