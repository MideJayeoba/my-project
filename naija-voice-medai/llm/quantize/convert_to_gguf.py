"""Convert target instruction model checkpoints into 4-bit GGUF artifacts.

Intended for BioMistral-7B or Gemma-2B-Instruct conversion through llama.cpp.
"""

from pathlib import Path


def convert(model_dir: Path, output_file: Path, quantization: str = "q4_k_m") -> None:
    """Document conversion intent for reproducible quantization runs.

    TODO: call llama.cpp conversion utilities in an environment with source models.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        f"Conversion plan: model={model_dir} quantization={quantization}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    convert(Path("models/gemma-2b-instruct"), Path("models/gemma-2b-instruct-q4.gguf"))
    print("GGUF conversion scaffold complete.")
