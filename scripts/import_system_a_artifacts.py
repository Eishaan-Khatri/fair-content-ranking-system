r"""Import the minimal System A artifacts needed by System B.

Example:
    python scripts/import_system_a_artifacts.py --system-a-path D:\\Projects\\narrative-intelligence-platform
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_PROCESSED = PROJECT_ROOT / "data" / "processed"
LOCAL_SYNTHETIC = PROJECT_ROOT / "data" / "synthetic"

REQUIRED_PROCESSED = [
    "item_fingerprints.parquet",
    "quality_scores.parquet",
    "session_features.parquet",
]
OPTIONAL_PROCESSED = [
    "item_embeddings.parquet",
]
OPTIONAL_SYNTHETIC = [
    "catalog.parquet",
]


def copy_if_present(src: Path, dst: Path, required: bool) -> dict:
    if not src.exists():
        if required:
            raise FileNotFoundError(f"Missing required System A artifact: {src}")
        return {"file": src.name, "status": "missing_optional", "source": str(src)}
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"file": src.name, "status": "copied", "source": str(src), "destination": str(dst), "bytes": dst.stat().st_size}


def import_artifacts(system_a_path: Path) -> list[dict]:
    source_processed = system_a_path / "data" / "processed"
    source_synthetic = system_a_path / "data" / "synthetic"
    if not source_processed.exists():
        raise FileNotFoundError(f"System A processed directory not found: {source_processed}")

    manifest: list[dict] = []
    for name in REQUIRED_PROCESSED:
        manifest.append(copy_if_present(source_processed / name, LOCAL_PROCESSED / name, required=True))
    for name in OPTIONAL_PROCESSED:
        manifest.append(copy_if_present(source_processed / name, LOCAL_PROCESSED / name, required=False))
    for name in OPTIONAL_SYNTHETIC:
        manifest.append(copy_if_present(source_synthetic / name, LOCAL_SYNTHETIC / name, required=False))

    manifest_path = PROJECT_ROOT / "data" / "system_a_import_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "imported_at": datetime.now(timezone.utc).isoformat(),
                "system_a_path": str(system_a_path),
                "artifacts": manifest,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy System A artifacts into this standalone System B repository.")
    parser.add_argument("--system-a-path", type=Path, required=True, help="Path to narrative-intelligence-platform checkout.")
    args = parser.parse_args()
    manifest = import_artifacts(args.system_a_path.resolve())
    copied = sum(1 for row in manifest if row["status"] == "copied")
    missing = [row["file"] for row in manifest if row["status"] == "missing_optional"]
    print(f"[OK] Copied {copied} System A artifacts into {PROJECT_ROOT}")
    if missing:
        print(f"[WARN] Optional artifacts missing: {', '.join(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

