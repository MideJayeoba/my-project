"""Evaluate clinical relevance of generated guidance on AfriMed-QA subset."""


def score_guidance(predicted_answer: str, reference_answer: str) -> float:
    """Simple lexical overlap baseline for thesis iteration tracking.

    TODO: replace with rubric-based clinician evaluation and semantic scoring.
    """
    p = set(predicted_answer.lower().split())
    r = set(reference_answer.lower().split())
    return len(p & r) / max(len(r), 1)
