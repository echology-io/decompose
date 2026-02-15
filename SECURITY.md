# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in Decompose, please report it privately:

**Email:** kyle@echology.io

**Subject:** `[SECURITY] Decompose — <brief description>`

Do not open a public issue for security vulnerabilities.

## Response

We will acknowledge receipt within 48 hours and aim to release a fix within 7 days for critical issues.

## Scope

Security-relevant areas of Decompose:

- **SSRF protection** in `decompose_url` (URL validation, IP blocklist)
- **Input validation** (max input size, parameter clamping)
- **ReDoS resistance** (bounded regex patterns)

## Out of Scope

- Decompose processes text locally and makes no outbound API calls (except `decompose_url` which fetches user-specified URLs)
- No authentication, no stored credentials, no user data persistence
- Classification accuracy is not a security concern (it's a preprocessing tool, not a security gate)
