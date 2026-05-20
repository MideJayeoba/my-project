"""ASR inference adapter for local transcription requests."""

from pathlib import Path


def transcribe_audio(audio_path: Path) -> str:
    """Transcribe one audio file with the fine-tuned ASR model.

    TODO: load checkpoint and run batched/streaming inference.
    """
    return f"[stub-transcript] received {audio_path.name}"
