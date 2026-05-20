# System Architecture

## Runtime flow
1. Browser captures microphone audio in a voice-only React interface.
2. Audio blob is posted to `POST /transcribe` in FastAPI.
3. ASR module returns transcript adapted for Nigerian-accented, code-switched speech.
4. Idiom mapping layer normalizes colloquial expressions to clinical terminology.
5. Transcript and retrieved context are sent to `POST /reason` for LLM+RAG inference.
6. Guidance text is posted to `POST /speak` and converted to spoken audio.
7. Browser auto-plays returned audio as the response.

## Deployment boundary
- Hosted inside PHC local network.
- No internet required during inference.
- Patient-sensitive data stays on-device/LAN.
