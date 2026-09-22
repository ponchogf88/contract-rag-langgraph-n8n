from fastapi import FastAPI
from pydantic import BaseModel
from .corpus import load_chunks
from .retrieve import build_index
from .graph import run_pipeline
from .classify import classify

app = FastAPI(title="Contract RAG Intake")

class Intake(BaseModel):
    filename: str = "upload.md"
    text: str
    query: str = "Resume obligaciones clave, ley aplicable y transferencias de datos."

@app.on_event("startup")
def startup():
    build_index(load_chunks())

@app.post("/classify")
def classify_endpoint(payload: Intake):
    return classify(payload.text).model_dump()

@app.post("/ask")
def ask(payload: Intake):
    return run_pipeline(payload.text, payload.query).model_dump()
