from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class DocType(str, Enum):
    NDA = "NDA"
    MSA = "MSA"
    DPA = "DPA"
    CREDIT = "CREDIT"
    OTHER = "OTHER"

class RiskFlag(str, Enum):
    UNLIMITED_LIABILITY = "unlimited_liability"
    OPEN_DATA_TRANSFER = "open_data_transfer"
    MISSING_GOVERNING_LAW = "missing_governing_law"
    AUTO_RENEW_SILENT = "auto_renew_silent"
    PII_PRESENT = "pii_present"
    HIGH_RISK_PROCESSING = "high_risk_processing"

class Classification(BaseModel):
    doc_type: DocType
    jurisdiction: str = "unknown"
    confidence: float = 0.0
    risk_flags: List[RiskFlag] = Field(default_factory=list)
    summary: str = ""

class Chunk(BaseModel):
    id: str
    doc_id: str
    doc_type: DocType
    text: str
    score: float = 0.0

class Answer(BaseModel):
    query: str
    answer: str
    citations: List[str]
    residual_risk: str
    classification: Optional[Classification] = None
    refused: bool = False
