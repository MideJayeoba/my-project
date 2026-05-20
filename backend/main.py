"""Purpose: FastAPI entrypoint for orchestrating voice AI requests."""

from fastapi import FastAPI

app = FastAPI(title="Voice Medical AI Assistant API")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Purpose: simple health endpoint for local setup validation."""
    return {"status": "ok"}
