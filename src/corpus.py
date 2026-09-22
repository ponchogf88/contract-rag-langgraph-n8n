from pathlib import Path
from typing import List
from .models import Chunk, DocType

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "contracts"

def load_chunks() -> List[Chunk]:
    chunks: List[Chunk] = []
    mapping = {
        "nda_sample.md": DocType.NDA,
        "msa_sample.md": DocType.MSA,
        "dpa_sample.md": DocType.DPA,
        "credit_addendum.md": DocType.CREDIT,
    }
    for filename, doc_type in mapping.items():
        path = DATA_DIR / filename
        text = path.read_text(encoding="utf-8")
        parts = [p.strip() for p in text.split("\n\n") if p.strip()]
        for i, part in enumerate(parts):
            chunks.append(Chunk(id=f"{path.stem}-{i}", doc_id=path.stem, doc_type=doc_type, text=part))
    return chunks
