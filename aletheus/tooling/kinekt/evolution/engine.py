"""Governed repository evolution engine."""

from __future__ import annotations

from pathlib import Path

from .backup import create_backup
from .executor import apply_plan
from .loader import load_plan
from .models import EvolutionResult
from .planner import validate_plan
from .reporting import write_result
from .rollback import rollback_manifest
from .validation import run_validation


class EvolutionEngine:
    def __init__(self, root: Path, output: Path) -> None:
        self.root = root.resolve()
        self.output = output.resolve()

    def validate(self, plan_path: Path) -> EvolutionResult:
        plan = load_plan(plan_path)
        validate_plan(self.root, plan)
        result = EvolutionResult(
            plan_id=plan.plan_id,
            mode="validate",
            status="validated",
        )
        write_result(result, self.output)
        return result

    def apply(self, plan_path: Path, *, approved: bool) -> EvolutionResult:
        if not approved:
            raise PermissionError(
                "Applying an evolution plan requires explicit approval."
            )

        plan = load_plan(plan_path)
        validate_plan(self.root, plan)
        backup_root, manifest_path = create_backup(self.root, plan)

        result = EvolutionResult(
            plan_id=plan.plan_id,
            mode="apply",
            status="running",
            backup_directory=str(backup_root),
            rollback_manifest=str(manifest_path),
        )

        try:
            result.changed_paths = apply_plan(self.root, plan)
            result.commands = run_validation(self.root, plan.validation)
            failures = [
                command for command in result.commands if command.returncode != 0
            ]
            if failures:
                rollback_manifest(manifest_path)
                result.status = "rolled_back"
                result.notes.append(
                    "Validation failed; repository files were restored."
                )
            else:
                result.status = "applied"
        except (OSError, ValueError, RuntimeError):
            rollback_manifest(manifest_path)
            result.status = "rolled_back"
            result.notes.append("Execution failed; repository files were restored.")
            write_result(result, self.output)
            raise

        write_result(result, self.output)
        return result
