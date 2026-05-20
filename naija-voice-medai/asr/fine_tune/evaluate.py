"""Evaluate ASR quality using WER against held-out Akure and AfriSpeech splits."""

from pathlib import Path
from jiwer import wer


def compute_wer(reference_texts: list[str], hypothesis_texts: list[str]) -> float:
    """Return WER score for two aligned transcript lists."""
    return wer(reference_texts, hypothesis_texts)


def main() -> None:
    """Starter CLI for ASR eval workflow.

    TODO: load predictions from fine-tuned model and compare to baseline model.
    """
    refs = ["patient reports fever and headache"]
    hyps = ["patient reports fever and hedache"]
    score = compute_wer(refs, hyps)
    print(f"Sample WER: {score:.3f} | reports_dir={Path('evaluation')}")


if __name__ == "__main__":
    main()
