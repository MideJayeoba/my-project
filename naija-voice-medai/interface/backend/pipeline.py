"""Pipeline coordinator for ASR -> idiom mapping -> LLM/RAG -> TTS workflow."""

from dataclasses import dataclass


@dataclass
class PipelineResult:
    """Container for output from one end-to-end voice query cycle."""

    transcript: str
    guidance_text: str


def run_pipeline(transcript: str) -> PipelineResult:
    """Run a simplified pipeline skeleton to be expanded in later phases."""
    # TODO: map idioms (llm/idiom_map), run rag+reason (llm/inference/reason.py).
    guidance = "Please rest, hydrate, and visit the PHC today if symptoms persist or worsen."
    return PipelineResult(transcript=transcript, guidance_text=guidance)
