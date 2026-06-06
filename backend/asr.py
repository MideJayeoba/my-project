"""ASR client that delegates transcription to an external Whisper service."""

import os
import httpx
from typing import Optional

# Set ASR_SERVICE_URL to your running Colab ngrok URL.
# Falls back to Hugging Face Inference API if not set (requires HF_API_TOKEN).
ASR_SERVICE_URL: Optional[str] = os.getenv("ASR_SERVICE_URL")
HF_API_TOKEN: Optional[str] = os.getenv("HF_API_TOKEN")

_HF_WHISPER_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

_TIMEOUT = 120  # seconds — large model can be slow on first call (model warm-up)


async def transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    """Send audio bytes to the ASR service and return the transcript string.

    Tries ASR_SERVICE_URL (Colab) first; falls back to HuggingFace Inference API.
    Returns an empty string if no service is configured or transcription fails.
    """
    if ASR_SERVICE_URL:
        return await _transcribe_colab(audio_bytes, filename)

    if HF_API_TOKEN:
        return await _transcribe_huggingface(audio_bytes)

    return ""


async def _transcribe_colab(audio_bytes: bytes, filename: str) -> str:
    base_url = ASR_SERVICE_URL.rstrip("/")
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            response = await client.post(
                f"{base_url}/transcribe",
                files={"audio": (filename, audio_bytes, "audio/webm")},
            )
            response.raise_for_status()
            return response.json().get("transcript", "")
    except Exception as exc:
        print(f"[ASR] Colab transcription failed: {exc}")
        return ""


async def _transcribe_huggingface(audio_bytes: bytes) -> str:
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            response = await client.post(
                _HF_WHISPER_URL,
                headers={"Authorization": f"Bearer {HF_API_TOKEN}"},
                content=audio_bytes,
            )
            response.raise_for_status()
            data = response.json()
            # HF returns {"text": "..."} for whisper models
            return data.get("text", "")
    except Exception as exc:
        print(f"[ASR] HuggingFace transcription failed: {exc}")
        return ""
