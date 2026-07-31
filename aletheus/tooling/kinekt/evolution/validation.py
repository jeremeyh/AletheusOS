"""Post-apply repository validation."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .models import CommandResult, ValidationSpec


def _run(root: Path, command: list[str]) -> CommandResult:
    completed = subprocess.run(
        command,
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
    )
    return CommandResult(
        command=tuple(command),
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def run_validation(root: Path, spec: ValidationSpec) -> list[CommandResult]:
    results: list[CommandResult] = []

    if spec.ruff_targets:
        results.append(_run(root, ["ruff", "check", *spec.ruff_targets]))
        results.append(_run(root, ["ruff", "format", "--check", *spec.ruff_targets]))

    if spec.compile_targets:
        results.append(
            _run(root, ["python", "-m", "compileall", *spec.compile_targets])
        )

    if spec.pytest_targets:
        results.append(_run(root, ["pytest", "-q", *spec.pytest_targets]))

    return results
