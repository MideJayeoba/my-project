"""Local text-to-speech synthesis adapter for offline-friendly deployments."""

import io
import wave


def synthesize_stub_wav(text: str, duration_seconds: float = 1.5) -> bytes:
    """Return a short silent WAV placeholder while TTS integration is pending."""
    sample_rate = 16000
    frame_count = int(sample_rate * duration_seconds)
    silence = b"\x00\x00" * frame_count

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(silence)
    return buffer.getvalue()
