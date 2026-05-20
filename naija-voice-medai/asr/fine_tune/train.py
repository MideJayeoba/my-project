"""Fine-tuning entrypoint for domain-adapted Nigerian medical ASR.

Expected stack: HuggingFace Trainer + PyTorch, with mixed precision and
validation logging for WER and code-switch robustness.
"""

from pathlib import Path
import yaml


def load_config(config_path: Path) -> dict:
    """Load YAML hyperparameters for reproducible training runs."""
    return yaml.safe_load(config_path.read_text(encoding="utf-8"))


def main() -> None:
    """Initialize datasets/model/trainer and start fine-tuning.

    TODO: wire model choice between NaijaEnglish-ASR-v1.0 and SBPN-Base.
    """
    config = load_config(Path(__file__).with_name("config.yaml"))
    print(f"Loaded ASR config for checkpoint: {config['model_checkpoint']}")


if __name__ == "__main__":
    main()
