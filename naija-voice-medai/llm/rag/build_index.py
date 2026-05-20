"""Build FAISS index from validated PHC clinical knowledge artifacts."""

from pathlib import Path
import json


def build_index(source_json: Path, index_dir: Path) -> Path:
    """Persist a starter index metadata file before FAISS integration."""
    index_dir.mkdir(parents=True, exist_ok=True)
    entries = json.loads(source_json.read_text(encoding="utf-8"))
    target = index_dir / "index_metadata.json"
    target.write_text(
        json.dumps({"document_count": len(entries), "source": str(source_json)}, indent=2),
        encoding="utf-8",
    )
    return target


if __name__ == "__main__":
    p = build_index(Path("llm/rag/knowledge_base/phc_conditions.json"), Path("llm/rag/index"))
    print(f"Index scaffold metadata written to: {p}")
