"""Backup and rollback manifest creation."""

from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import EvolutionPlan
from .paths import resolve_inside


def create_backup(root: Path, plan: EvolutionPlan) -> tuple[Path, Path]:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    backup_root = (
        root / ".aletheus_backups" / "kinekt_evolution" / f"{stamp}_{plan.plan_id}"
    )
    backup_root.mkdir(parents=True, exist_ok=False)

    manifest: dict[str, Any] = {
        "plan_id": plan.plan_id,
        "repository": str(root),
        "backup_root": str(backup_root),
        "entries": [],
    }

    for operation in plan.operations:
        source = resolve_inside(root, operation.path)
        entry: dict[str, Any] = {
            "path": operation.path,
            "existed": source.exists(),
        }
        if source.is_file():
            backup_path = backup_root / "files" / operation.path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, backup_path)
            entry["backup"] = str(backup_path)
        manifest["entries"].append(entry)

        if operation.operation == "move_file" and operation.destination:
            manifest["entries"].append(
                {
                    "path": operation.destination,
                    "existed": False,
                }
            )

    manifest_path = backup_root / "rollback.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return backup_root, manifest_path
