from pathlib import Path
import json
import typer
from rich import print
from .corpus import load_chunks, DATA_DIR
from .retrieve import build_index
from .graph import run_pipeline

app = typer.Typer()

@app.command()
def main(query: str = "What is the governing law and how is personal data transferred?", doc: str = "dpa_sample.md"):
    chunks = load_chunks()
    build_index(chunks)
    raw = (DATA_DIR / doc).read_text(encoding="utf-8")
    answer = run_pipeline(raw_text=raw, query=query)
    print(answer.model_dump())
    Path("logs").mkdir(exist_ok=True)
    with open("logs/audit.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(answer.model_dump(), ensure_ascii=False) + "\n")

if __name__ == "__main__":
    app()
