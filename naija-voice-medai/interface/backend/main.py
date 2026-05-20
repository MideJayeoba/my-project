"""FastAPI API surface for voice-in/voice-out medical assistant flows."""

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import io

from .pipeline import run_pipeline
from .tts import synthesize_stub_wav


class TranscribeResponse(BaseModel):
    """Typed response payload for ASR transcript output."""

    transcript: str


class ReasonRequest(BaseModel):
    """Input payload carrying recognized user utterance text."""

    transcript: str = Field(min_length=1, description="ASR transcript for clinical guidance")


class ReasonResponse(BaseModel):
    """Typed response for LLM reasoning output."""

    guidance: str
    safety_note: str


class SpeakRequest(BaseModel):
    """Input payload carrying guidance text for speech synthesis."""

    text: str = Field(min_length=1, description="Guidance text to synthesize")


app = FastAPI(title="Naija Voice MedAI Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(file: UploadFile = File(...)) -> TranscribeResponse:
    """Accept uploaded audio and return ASR transcript text.

    TODO: call `asr/inference/transcribe.py` with saved/streamed audio bytes.
    """
    _ = await file.read()
    transcript = f"Received audio file: {file.filename or 'recording.webm'}"
    return TranscribeResponse(transcript=transcript)


@app.post("/reason", response_model=ReasonResponse)
async def reason(payload: ReasonRequest) -> ReasonResponse:
    """Generate grounded clinical guidance from transcript text.

    TODO: call idiom mapping (`llm/idiom_map`) + reasoning (`llm/inference/reason.py`).
    """
    result = run_pipeline(payload.transcript)
    return ReasonResponse(
        guidance=result.guidance_text,
        safety_note="This assistant supports triage only and does not replace clinician judgment.",
    )


@app.post("/speak")
async def speak(payload: SpeakRequest) -> StreamingResponse:
    """Synthesize speech audio for browser playback.

    TODO: replace stub with `interface/backend/tts.py` engine implementation (pyttsx3/Coqui).
    """
    wav_bytes = synthesize_stub_wav(payload.text)
    return StreamingResponse(io.BytesIO(wav_bytes), media_type="audio/wav")
