"""Retriever interface for grounding LLM responses with PHC knowledge."""

import json
from pathlib import Path


def retrieve(query: str, knowledge_path: Path, top_k: int = 3) -> list[dict]:
    """Return naive keyword-matched entries as a placeholder retriever."""
    records = json.loads(knowledge_path.read_text(encoding="utf-8"))
    q = query.lower()
    matches = [r for r in records if any(k.lower() in q for k in r["clinical_keywords"])]
    return matches[:top_k]
