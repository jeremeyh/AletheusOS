"""Apply approved evolution operations."""

from __future__ import annotations

import shutil
from pathlib import Path

from .models import EvolutionPlan
from .paths import resolve_inside


def apply_plan(root: Path, plan: EvolutionPlan) -> list[str]:
    changed: list[str] = []

    for operation in plan.operations:
        source = resolve_inside(root, operation.path)

        if operation.operation == "replace_text":
            text = source.read_text(encoding="utf-8")
            source.write_text(
                text.replace(operation.old or "", operation.new or "", 1),
                encoding="utf-8",
            )
            changed.append(operation.path)

        elif operation.operation == "write_file":
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(operation.content or "", encoding="utf-8")
            changed.append(operation.path)

        elif operation.operation == "move_file":
            destination = resolve_inside(root, operation.destination or "")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            changed.extend([operation.path, operation.destination or ""])

    return changed
