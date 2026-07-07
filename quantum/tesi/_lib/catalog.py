"""Load thesis paper catalog and resolve local data paths."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def project_root() -> Path:
    """Repo root (MASTER OQI)."""
    return Path(__file__).resolve().parents[3]


def thesis_data_dir() -> Path:
    return project_root() / "data" / "100_TESI"


def load_catalog(catalog_path: Path | None = None) -> dict[str, Any]:
    path = catalog_path or (Path(__file__).resolve().parent.parent / "papers_catalog.yaml")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_local_pdfs(data_dir: Path | None = None) -> list[Path]:
    root = data_dir or thesis_data_dir()
    if not root.exists():
        return []
    return sorted(root.rglob("*.pdf"))


def summarize_catalog(catalog: dict[str, Any]) -> dict[str, int]:
    """Paper counts per level id."""
    out: dict[str, int] = {}
    for level in catalog.get("levels", []):
        out[level["id"]] = len(level.get("papers", []))
    return out
