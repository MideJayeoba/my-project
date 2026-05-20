# Voice-based Medical AI Assistant for Low-Literacy Communities in Nigeria

This repository is the starter scaffold for a final-year CS thesis project focused on a **voice-first medical assistant**.

## Project goal
The assistant supports users who may not be comfortable reading or typing by using a speech-only interaction loop:

1. User speaks
2. ASR transcribes speech
3. LLM reasons over the request
4. TTS speaks a response back

> Product direction: no user-facing text in the final interface.

## Repository structure
- `backend/` — FastAPI service exposing API endpoints and orchestration logic.
- `frontend/` — React app used to prototype voice capture/playback UI.
- `asr/` — automatic speech recognition experiments and model adapters.
- `llm/` — local LLM inference adapters and prompt logic.
- `data/` — datasets, prompts, and generated artifacts (kept out of git where needed).

## Basic architecture
- **Frontend (React):** records user audio and sends it to backend APIs.
- **Backend (FastAPI):** orchestrates ASR -> LLM -> TTS pipeline.
- **ASR module:** wraps HuggingFace ASR models/pipelines.
- **LLM module:** wraps local LLM inference runtime.
- **TTS (future module):** converts model responses to speech audio.

## Local setup
### 1) Backend
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

With backend running on `http://127.0.0.1:8000` and frontend on `http://localhost:5173`, you can start wiring voice endpoints end-to-end.
