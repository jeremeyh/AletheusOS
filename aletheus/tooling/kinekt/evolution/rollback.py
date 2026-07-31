"""Restore files from an evolution rollback manifest."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .paths import resolve_inside


def rollback_manifest(manifest_path: Path) -> list[str]:
    payload: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = Path(payload["repository"]).resolve()
    restored: list[str] = []

    for entry in reversed(payload["entries"]):
        relative = str(entry["path"])
        target = resolve_inside(root, relative)
        existed = bool(entry["existed"])

        if existed:
            backup = Path(entry["backup"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, target)
        elif target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        restored.append(relative)

    return restored
