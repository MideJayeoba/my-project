"""Audio preprocessing pipeline for PHC voice recordings.

Planned steps: load raw WAV, denoise, loudness-normalize, VAD-based segmenting,
and export segment metadata for ASR training and error analysis.
"""

from pathlib import Path


def preprocess_directory(raw_dir: Path, processed_dir: Path) -> None:
    """Prepare a raw recording folder for ASR training.

    TODO: integrate librosa + webrtcvad/noisereduce based processing.
    """
    processed_dir.mkdir(parents=True, exist_ok=True)
    # TODO: iterate WAV files, run denoise+normalization+segmentation.
    print(f"Preprocessing queued from {raw_dir} -> {processed_dir}")


if __name__ == "__main__":
    preprocess_directory(Path("data/raw"), Path("data/processed"))
