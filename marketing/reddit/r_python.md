# r/Python

**Flair:** I Made This

**Title:** (98 chars)
```
I built Decompose – a pure-regex document classifier that scores authority, risk, and attention
```

---

**Body:**

## What My Project Does

Decompose is a Python library that splits text into semantic units and classifies each one — authority level, risk category, attention score, entity extraction, and irreducibility flags. It uses pure stdlib regex. No LLM, no API key, no GPU. Deterministic — same input always produces same output. ~14ms average per document.

```python
from decompose import decompose_text
result = decompose_text(open("spec.md").read())  # ~14ms avg
```

Each unit gets:

- **Authority**: mandatory, prohibitive, directive, permissive, informational (RFC 2119 keyword detection)
- **Risk**: safety_critical, security, compliance, financial, contractual, advisory, informational
- **Attention**: 0.0-10.0 score (authority weight × risk multiplier)
- **Entities**: standards, codes, regulations extracted via regex
- **Irreducibility**: must this unit be preserved verbatim?

Also works as an MCP server for Claude, Cursor, etc:

```bash
pip install decompose-mcp
python -m decompose --serve
```

## Target Audience

Developers building LLM pipelines, RAG systems, or agent workflows that process specs, contracts, or regulatory documents. It's a preprocessor — runs before your model so the model spends tokens on the parts that matter instead of boilerplate.

## Comparison

Unlike LLM-based classifiers (zero-shot with GPT/Claude, fine-tuned BERT, etc.), Decompose is fully deterministic, runs offline, and costs nothing per call. The tradeoff: no nuance, no cross-document reasoning, no intent classification, no domain-specific language that doesn't match standard patterns. The LLM still does the hard work — Decompose handles the easy classification so your model can focus on the hard reasoning.

## Benchmarks

I ran the entire Anthropic prompt engineering docs (10 pages, 20K chars) through it — 43 semantic units in 34ms. The financial analysis section correctly flagged as irreducible with exact dollar amounts extracted. The security warning from the MCP spec scored 4.5/10 attention while the overview scored 0.0. 1,064 chars/ms on Apple Silicon.

## What You Do After Classification

The output is structured JSON. Filter by attention score to decide what goes to the LLM. Route by risk category to different processing chains. Use the irreducibility flag to protect content your model must not paraphrase. Runnable examples in the `examples/` directory on GitHub.

Happy to answer questions about the regex architecture or the classification patterns.

---

**FIRST COMMENT (post immediately after):**

Links:

- GitHub: https://github.com/echology-io/decompose
- PyPI: https://pypi.org/project/decompose-mcp/
- Listed on the official MCP Registry
