"""Capture and catalog structured voice recording sessions in Akure PHCs.

This module defines starter utilities for consent-first, metadata-rich recording
sessions used to collect medical Nigerian-accented English and Yoruba/Pidgin
code-switched speech for ASR fine-tuning.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json


@dataclass
class SessionMeta:
    """Metadata required to audit and reuse a recording session safely."""

    session_id: str
    location: str
    interviewer: str
    language_mix: str
    consent_obtained: bool
    started_at: str


def create_session_manifest(output_dir: Path, metadata: SessionMeta) -> Path:
    """Persist one session manifest in JSON format for later preprocessing."""
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{metadata.session_id}.json"
    target.write_text(json.dumps(metadata.__dict__, indent=2), encoding="utf-8")
    return target


if __name__ == "__main__":
    demo = SessionMeta(
        session_id=f"akure-phc-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        location="Akure South PHC",
        interviewer="research-assistant-01",
        language_mix="Nigerian English + Yoruba + Pidgin",
        consent_obtained=True,
        started_at=datetime.now().isoformat(),
    )
    path = create_session_manifest(Path("data/raw"), demo)
    print(f"Created session manifest: {path}")
