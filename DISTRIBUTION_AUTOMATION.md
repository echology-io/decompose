# Decompose — Distribution Automation Map

Everything below can be automated via CI, scripts, or scheduled jobs. No human login required after initial setup.

---

## Already Automated (Done)

| What | How | Status |
|------|-----|--------|
| Lint on push | `.github/workflows/ci.yml` — ruff check | Done |
| Test on push | `.github/workflows/ci.yml` — pytest across Python 3.10-3.13 | Done |
| Publish to PyPI on tag | `.github/workflows/publish.yml` — triggered by `v*` tags | Done |
| MCP server registration | `pyproject.toml` entry-point `[project.entry-points."mcp.servers"]` | Done |
| CLI entrypoint | `pyproject.toml` `[project.scripts]` — `decompose` command | Done |

---

## Can Automate Next

### 1. Benchmark Suite (CI-Publishable Metrics)
**What:** Automated benchmarks that produce shareable numbers.
**Why:** "Engineers don't share vibes. They share performance."

```yaml
# .github/workflows/benchmark.yml
- Run decompose against 5 reference documents (bundled in tests/fixtures/)
- Measure: processing_ms, token_reduction_pct, units_generated, standards_found
- Output: benchmark.json artifact
- Comment results on PRs (via github-script action)
```

**Automate:** Add `tests/fixtures/` with 3-5 sample documents. Write `benchmarks/run.py`. CI publishes results as a job artifact. README badge links to latest benchmark.

### 2. README Badge Generation
**What:** Dynamic badges showing test status, version, downloads.

```markdown
![Tests](https://github.com/echology-io/decompose/actions/workflows/ci.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/decompose)
![Downloads](https://img.shields.io/pypi/dm/decompose)
![License](https://img.shields.io/badge/license-proprietary-blue)
```

**Automate:** Add to README.md header. Shields.io generates dynamically. Zero maintenance.

### 3. Changelog Generation
**What:** Auto-generate CHANGELOG.md from commit messages on release.

```yaml
# In publish.yml, before build step:
- uses: orhun/git-cliff-action@v4
  with:
    config: cliff.toml
    args: --latest
```

**Automate:** Add `cliff.toml` config. Changelog updates on every tag.

### 4. GitHub Pages Landing Page
**What:** Static site at echology.io/decompose (or decompose.new).

```
docs/
├── index.html    # Single page: hero, demo GIF, install, before/after
├── CNAME         # Custom domain
└── style.css     # Minimal
```

**Automate:** GitHub Actions deploys `docs/` to `gh-pages` branch on push to main. Human only needs to set up DNS once (in HUMAN_TASKS.md).

### 5. Social Preview Image
**What:** Auto-generate the Open Graph image shown when repo is shared on social.

**Automate:** Use GitHub's built-in social preview OR generate via a simple HTML→PNG script in CI. Set once, never touch again.

### 6. Dependabot / Renovate
**What:** Auto-update the `mcp` dependency when new versions ship.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: pip
    directory: "/"
    schedule:
      interval: weekly
```

**Automate:** Add file, done. PRs auto-created, CI tests them.

### 7. Release Drafter
**What:** Auto-draft GitHub Releases from merged PRs.

```yaml
# .github/workflows/release-drafter.yml
- uses: release-drafter/release-drafter@v6
```

**Automate:** Categorizes PRs by label, drafts release notes. Human just clicks "Publish."

---

## Can Automate with More Effort

### 8. OpenClaw Skill Template Generator
**What:** A script that generates a ready-to-fork OpenClaw agent config using decompose.

```bash
# decompose init-skill > openclaw_decompose.json
```

**Automate:** Add `decompose init-skill` CLI subcommand. Outputs a complete agent config file. Users fork it.

### 9. Weekly PyPI Stats Reporter
**What:** GitHub Action that fetches PyPI download stats weekly and commits to `stats/`.

**Automate:** Scheduled workflow (cron weekly). Fetches from pypistats.org API. Commits JSON. README badge auto-updates.

### 10. Template Repository Auto-Generator
**What:** For each of the 3 workflow templates (Decompose→Plan→Execute, etc.), auto-generate a template repo with:
- README
- Agent config
- Example prompt
- Sample input/output

**Automate:** Script reads template definitions from `templates/` dir, generates repos via `gh repo create --template`. Run once per template update.

---

## Distribution Channels — Automation Potential

| Channel | Human Required | Automatable |
|---------|---------------|-------------|
| **PyPI** | Initial token setup | Publish on tag (done) |
| **GitHub** | Initial repo create | CI, badges, releases, dependabot |
| **OpenClaw** | Skill submission, builder DMs | Skill config generation, template repos |
| **X/Twitter** | Write thread, record demo | Schedule posts via Buffer/Typefully |
| **LinkedIn** | Write post | Schedule via native scheduler |
| **Reddit** | Write posts, engage comments | Nothing (authentic engagement required) |
| **Hacker News** | Submit, engage | Nothing (authentic engagement required) |
| **Blog** | Write article | Auto-publish from repo via dev.to API |
| **Landing page** | DNS setup, demo GIF | GitHub Pages deploy (done) |
| **Benchmarks** | Choose reference docs | CI runs, publishes results |
| **Changelog** | Nothing | git-cliff on release |
| **Stats** | Nothing | Weekly cron job |

---

## Priority Order

1. **Benchmark suite** — Creates the shareable metrics ("78% token reduction, 2ms processing")
2. **README badges** — 5 minutes, instant credibility signal
3. **Dependabot** — 1 file, keeps deps current forever
4. **GitHub Pages** — Landing page for the domain you already own
5. **Release drafter** — Polish for future releases
6. **Changelog** — Auto-generated, builds trust
7. **Skill template generator** — Reduces friction for OpenClaw users
8. **Stats reporter** — Track growth passively
