import os
from typing import List
from .models import Answer, Classification, Chunk, DocType

REFUSAL = (
    "No puedo afirmar una conclusion juridica fuera del corpus ruteado. "
    "Falta documento clasificado o los fragmentos no cubren la pregunta."
)

def generate_answer(query: str, classification: Classification, chunks: List[Chunk]) -> Answer:
    if classification.doc_type == DocType.OTHER or not chunks:
        return Answer(query=query, answer=REFUSAL, citations=[], residual_risk="Unrouted document — human review required before any legal reliance.", classification=classification, refused=True)
    citations = [c.id for c in chunks]
    context = "\n\n".join(f"[{c.id}] {c.text}" for c in chunks)
    text = _llm(query, context, classification) if os.getenv("OPENAI_API_KEY") else _template(query, chunks, classification)
    return Answer(query=query, answer=text, citations=citations, residual_risk=_residual(classification), classification=classification, refused=False)

def _template(query: str, chunks: List[Chunk], classification: Classification) -> str:
    bullets = "\n".join(f"- ({c.id}) {c.text[:280]}" for c in chunks[:3])
    flags = ", ".join(f.value for f in classification.risk_flags) or "none"
    return (
        f"Respuesta grounded al corpus {classification.doc_type.value} "
        f"(jurisdiccion detectada: {classification.jurisdiction}).\n\n"
        f"Pregunta: {query}\n\nHallazgos con citas:\n{bullets}\n\n"
        f"Risk flags de intake: {flags}\nEsta salida no sustituye revision de counsel."
    )

def _llm(query: str, context: str, classification: Classification) -> str:
    from urllib.request import Request, urlopen
    import json
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    payload = {"model": model, "messages": [{"role": "system", "content": "You are a compliance-first legal document assistant. Answer ONLY from the provided chunks. Cite chunk ids. If the chunks do not support the answer, refuse. Document type: " + classification.doc_type.value + "."}, {"role": "user", "content": f"Question: {query}\n\nChunks:\n{context}"}], "temperature": 0}
    req = Request("https://api.openai.com/v1/chat/completions", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"})
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    return data["choices"][0]["message"]["content"]

def _residual(classification: Classification) -> str:
    if not classification.risk_flags:
        return "No automated high-risk flags. Counsel should still validate jurisdiction and defined terms."
    return "Flags require human review before relying on the answer: " + ", ".join(f.value for f in classification.risk_flags)
