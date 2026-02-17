# Examples

What to build after Decompose classifies your document.

## Scripts

**`rag_pipeline.py`** — Attention-filtered RAG. Decomposes a document and shows which units would enter your vector store (attention >= 2.0) vs. which get skipped. Replace `mock_embed()` with your real embedding function.

```bash
python examples/rag_pipeline.py
python examples/rag_pipeline.py path/to/your/spec.md
```

**`agent_router.py`** — Risk-based routing. Routes each unit to a different handler based on risk category: safety-critical, financial, compliance, or general. Low-attention units get skipped entirely.

```bash
python examples/agent_router.py
python examples/agent_router.py path/to/your/contract.md
```

**`cost_calculator.py`** — Token cost reduction. Measures how many units need LLM analysis vs. how many Decompose filters out. Prints before/after cost estimates at scale.

```bash
python examples/cost_calculator.py
python examples/cost_calculator.py path/to/your/document.md
```

**`compliance_audit.py`** — Deterministic audit trail. Prints the full classification for every unit — authority, risk, attention, entities, financials. Run it twice on the same input: same output every time.

```bash
python examples/compliance_audit.py
python examples/compliance_audit.py path/to/your/spec.md
```

## Requirements

```bash
pip install decompose-mcp
```

No other dependencies. Each script runs standalone.
