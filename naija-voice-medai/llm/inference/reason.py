"""Reasoning orchestration for quantized clinical guidance generation."""

from pathlib import Path

from llm.rag.retriever import retrieve


def generate_guidance(query: str, knowledge_path: str) -> dict:
    """Return grounded response payload for downstream TTS synthesis.

    TODO: replace template response with llama.cpp inference call.
    """
    evidence = retrieve(query=query, knowledge_path=Path(knowledge_path), top_k=3)
    guidance = (
        "This is triage support only. A PHC clinician should review persistent or severe symptoms."
    )
    return {"guidance": guidance, "evidence": evidence}
