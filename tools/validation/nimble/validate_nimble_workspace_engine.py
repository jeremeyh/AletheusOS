#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)


ENGINE_ROOT = (
    ROOT
    / "nimble/packages/workspace/src/engine"
)

REPORT = (
    ROOT
    / "reports/nimble/experience/"
    "workspace-engine-validation-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required_files = [
        "contracts.ts",
        "founder.ts",
        "index.ts",
        "layout.ts",
        "lifecycle.ts",
        "persistence.ts",
        "registry.ts",
        "validation.ts",
    ]

    for relative in required_files:
        if not (
            ENGINE_ROOT / relative
        ).is_file():
            failures.append(
                f"Missing Workspace Engine file: {relative}"
            )

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ENGINE_ROOT.rglob("*.ts")
    )

    concepts = [
        "Founder Console™",
        "Intelligence Instrumentation™",
        "WorkspaceRegistry",
        "WorkspaceSnapshot",
        "activity-rail",
        "status-bar",
        "floating",
        "detached",
        "founder",
    ]

    for concept in concepts:
        if concept not in combined:
            failures.append(
                f"Missing Workspace Engine concept: {concept}"
            )

    typecheck = subprocess.run(
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-workspace-engine",
        ],
        cwd=ROOT / "nimble",
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    if typecheck.returncode != 0:
        failures.append(
            "Workspace Engine typecheck failed."
        )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_at": datetime.now(
                    UTC
                ).isoformat(),
                "status": status,
                "failures": failures,
                "typecheck_stdout":
                    typecheck.stdout.strip(),
                "typecheck_stderr":
                    typecheck.stderr.strip(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ WORKSPACE ENGINE")
    print("=" * 72)
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    if typecheck.returncode != 0:
        print(typecheck.stdout)
        print(typecheck.stderr)

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
