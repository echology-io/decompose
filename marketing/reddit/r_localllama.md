# r/LocalLLaMA

**Flair:** Tools and Projects

**Title:** (97 chars)
```
You don't need an LLM to classify documents. Decompose does it in ~14ms with pure regex, no API.
```

---

**Body:**

I keep seeing people throw local models at document classification tasks where the answer is literally in the keywords.

"SHALL" means mandatory. "MUST NOT" means prohibitive. "MAY" means permissive. This isn't an opinion — it's RFC 2119, written in 1997 specifically to make these words unambiguous.

Decompose is a Python library that classifies text into semantic units using regex pattern matching:

- Authority level (mandatory/prohibitive/directive/permissive/informational)
- Risk category (safety_critical/security/compliance/financial)
- Attention score (0.0-10.0 — how much compute should an agent spend here?)
- Entity extraction (standards, codes, regulations)

Performance: ~14ms avg per document. 1,064 chars/ms on Apple Silicon. I ran the full Anthropic prompt engineering docs (10 pages, 20K chars) — 43 units in 34ms. The MCP Transport spec (live URL fetch) returned 14 units in 29ms with the security warning scoring 4.5/10 attention.

The insight isn't that regex is better than LLMs. It's that regex handles the easy classification so your local model can focus on the hard reasoning. Decompose runs *before* the LLM as a preprocessor. Your agent reads 2 high-attention units instead of 9 units of raw text.

```bash
pip install decompose-mcp
```

GitHub: https://github.com/echology-io/decompose

**What you do after classification:** The output is structured JSON. Filter by attention score to decide what goes to your local model. Route by risk category to different processing chains. Use the irreducibility flag to protect content your model must not paraphrase. Runnable examples in the `examples/` directory.

Honest about limitations: no nuance, no cross-document reasoning, no intent classification, no domain-specific language that doesn't match standard patterns. The LLM still does the hard work.
