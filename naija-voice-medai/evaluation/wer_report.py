"""Compute word error rate (WER) reports for ASR experiment outputs."""

from jiwer import wer


def report_wer(reference: list[str], prediction: list[str]) -> dict:
    """Return compact WER metrics dictionary for logging or dashboarding."""
    score = wer(reference, prediction)
    return {"wer": round(score, 4), "samples": len(reference)}
