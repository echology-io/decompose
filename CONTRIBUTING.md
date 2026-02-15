# Contributing to Decompose

Thanks for your interest in contributing.

## Reporting Issues

Open an issue at [github.com/echology-io/decompose/issues](https://github.com/echology-io/decompose/issues) with:

- A clear description of the problem
- Input text that reproduces it
- Expected vs actual output

## Development

```bash
git clone https://github.com/echology-io/decompose.git
cd decompose
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check . && ruff format --check .
```

## Pull Requests

1. Fork the repo and create a branch from `main`
2. Add tests for any new functionality
3. Ensure `pytest` and `ruff` pass
4. Open a PR with a clear description of what changed and why

## Scope

Decompose is intentionally minimal. We prioritize:

- **Correctness** over features
- **Determinism** over flexibility
- **Speed** over completeness

PRs that add LLM dependencies, external API calls, or non-deterministic behavior will not be accepted.

## License

By contributing, you agree that your contributions will be licensed under the same terms as the project (see [LICENSE](LICENSE)).
