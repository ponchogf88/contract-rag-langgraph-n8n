from typing import TypedDict, List
from .models import Classification, Chunk, Answer, DocType
from .classify import classify
from .retrieve import retrieve
from .generate import generate_answer

class State(TypedDict, total=False):
    raw_text: str
    query: str
    classification: Classification
    chunks: List[Chunk]
    answer: Answer

def node_classify(state: State) -> State:
    state["classification"] = classify(state["raw_text"])
    return state

def node_retrieve(state: State) -> State:
    doc_type = state["classification"].doc_type
    state["chunks"] = [] if doc_type == DocType.OTHER else retrieve(state["query"], doc_type)
    return state

def node_generate(state: State) -> State:
    state["answer"] = generate_answer(query=state["query"], classification=state["classification"], chunks=state.get("chunks", []))
    return state

def run_pipeline(raw_text: str, query: str) -> Answer:
    state: State = {"raw_text": raw_text, "query": query}
    node_classify(state)
    node_retrieve(state)
    node_generate(state)
    return state["answer"]

def build_langgraph():
    from langgraph.graph import StateGraph, END
    g = StateGraph(dict)
    g.add_node("classify", node_classify)
    g.add_node("retrieve", node_retrieve)
    g.add_node("generate", node_generate)
    g.set_entry_point("classify")
    g.add_edge("classify", "retrieve")
    g.add_edge("retrieve", "generate")
    g.add_edge("generate", END)
    return g.compile()
