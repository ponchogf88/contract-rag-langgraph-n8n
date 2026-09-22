# Contract RAG + Intelligent Document Processing (LangGraph + n8n)

Portfolio demo for **Legal Engineer / AI Workflow Architect** roles that ask for:

- RAG on legal documents
- intelligent document processing
- compliance-first routing (fintech / banking)
- LangGraph + n8n in production-shaped workflows

Built for applications like Lumenalta AI Engineer (Remote LATAM).

**Author:** Jesús A. Gutiérrez Flores — Legal Engineer, Monterrey, MX  
**Site:** https://jesus-a-gutierrezflores.ai.studio

---

## What this demonstrates

A contract intake pipeline that does **not** dump every PDF into a generic chatbot.

1. Ingest a contract (NDA, MSA, DPA, credit addendum).
2. Classify document type + jurisdiction + risk flags.
3. Route to the right retrieval corpus (compliance-first).
4. Answer with citations and a residual-risk note.
5. Optionally trigger the same flow from **n8n** (webhook → classify → RAG → Slack/email).

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m src.run_demo --query "What is the governing law and data-transfer clause?"
```

## n8n

Import `n8n/contract-intake-rag.json`.

## Disclaimer

Sample contracts are synthetic. Portfolio system, not legal advice.
