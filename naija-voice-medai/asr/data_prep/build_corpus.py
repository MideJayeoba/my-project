"""Merge local PHC speech corpus with external African speech resources.

This script is intended to align transcript formats and merge the primary Akure
corpus with an AfriSpeech-200 clinical subset for more robust ASR coverage.
"""

from pathlib import Path


def build_training_manifest(primary_manifest: Path, afrispeech_manifest: Path, output_manifest: Path) -> None:
    """Produce a single CSV/JSONL manifest consumed by fine-tuning scripts."""
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    # TODO: normalize schema (audio_path, transcript, language_tags, source).
    merged = "audio_path,transcript,language_tags,source\n"
    merged += f"# merge_from={primary_manifest}\n"
    merged += f"# merge_from={afrispeech_manifest}\n"
    output_manifest.write_text(merged, encoding="utf-8")


if __name__ == "__main__":
    build_training_manifest(
        Path("data/splits/primary.csv"),
        Path("data/splits/afrispeech200_clinical.csv"),
        Path("data/splits/train_manifest.csv"),
    )
    print("Training manifest scaffold generated.")
