from .models import Classification, DocType, RiskFlag

KEYWORDS = {
    DocType.NDA: ["non-disclosure", "confidential information", "receiving party"],
    DocType.MSA: ["master services", "statement of work", "service levels"],
    DocType.DPA: ["data processing", "sub-processor", "personal data", "gdpr"],
    DocType.CREDIT: ["credit limit", "default", "risk rating", "kyc"],
}

FLAG_RULES = [
    (RiskFlag.UNLIMITED_LIABILITY, ["unlimited liability", "no cap on liability"]),
    (RiskFlag.OPEN_DATA_TRANSFER, ["any country", "worldwide transfer", "unrestricted transfer"]),
    (RiskFlag.MISSING_GOVERNING_LAW, []),
    (RiskFlag.AUTO_RENEW_SILENT, ["automatic renewal", "auto-renew"]),
    (RiskFlag.PII_PRESENT, ["personal data", "identifiable", "kyc"]),
    (RiskFlag.HIGH_RISK_PROCESSING, ["credit decision", "automated decision", "profiling"]),
]

def classify(text: str) -> Classification:
    lower = text.lower()
    scores = {dt: sum(1 for k in keys if k in lower) for dt, keys in KEYWORDS.items()}
    doc_type = max(scores, key=scores.get) if max(scores.values()) > 0 else DocType.OTHER
    confidence = min(1.0, max(scores.values()) / 3) if scores else 0.0
    flags = []
    for flag, needles in FLAG_RULES:
        if any(n in lower for n in needles):
            flags.append(flag)
    if "governing law" not in lower and "ley aplicable" not in lower:
        flags.append(RiskFlag.MISSING_GOVERNING_LAW)
    jurisdiction = "unknown"
    for label in ["mexico", "méxico", "delaware", "england", "spain", "european union"]:
        if label in lower:
            jurisdiction = label
            break
    return Classification(doc_type=doc_type, jurisdiction=jurisdiction, confidence=confidence, risk_flags=flags, summary=f"{doc_type.value} candidate · {jurisdiction} · {len(flags)} risk flags")
