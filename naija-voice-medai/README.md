# Voice-based Medical AI Assistant for Low-Literacy Communities in Southwest Nigeria

This final-year Computer Science thesis project builds a voice-first medical assistant tailored for low-literacy communities in Akure, Ondo State. The system combines Nigerian-accent-aware ASR, grounded local LLM reasoning, and spoken responses so users can interact without reading or typing.

## Academic Context
- Institution: Olusegun Agagu University of Science and Technology (OAUSTECH)
- Department: Computer Science
- Project type: Final-year thesis

## Two-Phase Deployment Strategy

### Phase 1 — LAN-hosted web app (current)
- FastAPI backend and React frontend run on a local PHC server.
- Any phone/tablet/laptop on the same local network can use a browser to access the assistant.
- No internet is required for runtime inference.

### Phase 2 — Offline PWA (planned)
- Add service-worker based caching and offline-first app shell.
- Make the app installable on Android as a Progressive Web App.
- Complete migration steps are documented in `docs/phase2_pwa_plan.md`.

## Architecture Overview

`Browser mic → /transcribe → ASR → idiom map → /reason → LLM+RAG → /speak → TTS audio → browser playback`

## Key Model Choices

| Component | Candidate Model(s) | Runtime Choice | Rationale |
|---|---|---|---|
| ASR | NaijaEnglish-ASR-v1.0 (Whisper-based), SBPN-Base (120M) | Fine-tune whichever yields lower WER on Akure corpus | Both support adaptation to Nigerian-accented and code-switched speech under limited-resource conditions |
| Clinical Reasoning LLM | BioMistral-7B, Gemma 2B-Instruct | Quantized GGUF via llama.cpp | Enables local CPU-friendly inference while preserving useful instruction-following behavior |
| Inference Backend | llama.cpp | 4-bit GGUF | Reduces memory footprint for PHC hardware constraints and keeps inference fully local |

## Dataset Sources
- Primary Akure PHC corpus (consented local recordings)
- AfriSpeech-200 clinical subset (speech robustness augmentation)
- AfriMed-QA subset (clinical relevance evaluation)

## Setup and Run

```bash
cd naija-voice-medai
./scripts/setup_env.sh
./scripts/start_server.sh
./scripts/start_frontend.sh
```

Then open the printed LAN URL from the frontend server on any browser connected to the PHC network.

## Evaluation Metrics
- **ASR quality:** Word Error Rate (WER) on held-out test split
- **Reasoning relevance:** AfriMed-QA subset score
- **Human factors:** user trust score from structured field interviews

## Ethics and Privacy Note
All inference is designed for on-device/LAN execution inside the PHC environment. No patient data is transmitted to external servers during normal operation.
