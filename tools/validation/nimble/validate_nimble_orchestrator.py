#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _find_repo_root() -> Path:
    current = Path(__file__).resolve().parent

    while True:
        if (current / "pyproject.toml").is_file():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = _find_repo_root()

REPORT = ROOT / "reports" / "nimble" / "orchestrator" / "build-state-latest.json"


def main() -> int:
    failures: list[str] = []

    required = [
        "nimble/__init__.py",
        "nimble/orchestrator/__init__.py",
        "nimble/orchestrator/__main__.py",
        "nimble/orchestrator/cli.py",
        "nimble/orchestrator/discovery.py",
        "nimble/orchestrator/drift.py",
        "nimble/orchestrator/manifest.py",
        "nimble/orchestrator/models.py",
        "nimble/orchestrator/planner.py",
        "nimble/orchestrator/readiness.py",
        "nimble/orchestrator/report.py",
    ]

    for relative in required:
        if not (ROOT / relative).is_file():
            failures.append(f"Missing orchestrator file: {relative}")

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "nimble.orchestrator",
            "--root",
            str(ROOT),
            "--report",
            str(REPORT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    if result.returncode != 0:
        failures.append("Nimble Build Orchestrator execution failed.")

    if not REPORT.is_file():
        failures.append("Orchestrator state report was not generated.")
        report: dict[str, object] = {}
    else:
        try:
            report = json.loads(REPORT.read_text(encoding="utf-8"))
        except (
            OSError,
            json.JSONDecodeError,
        ) as error:
            failures.append(f"Unable to read orchestrator state report: {error}")
            report = {}

        if report.get("schema_version") != "1.0":
            failures.append("Invalid orchestrator report schema.")

        capabilities = report.get(
            "capabilities",
            [],
        )

        if not isinstance(
            capabilities,
            list,
        ):
            failures.append("Invalid capabilities section in orchestrator report.")
            capabilities = []

        capability_ids = {
            item.get("capability_id") for item in capabilities if isinstance(item, dict)
        }

        expected = {
            "experience-core",
            "react-primitives",
            "workspace-engine",
            "founder-console",
        }

        missing = expected - capability_ids

        if missing:
            failures.append(
                "Missing orchestrator capabilities: " + ", ".join(sorted(missing))
            )

    status = "PASS" if not failures else "FAIL"

    print("=" * 72)
    print("NIMBLE™ BUILD ORCHESTRATOR VALIDATION")
    print("=" * 72)
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    if result.stdout.strip():
        print()
        print(result.stdout.strip())

    if result.stderr.strip():
        print()
        print(result.stderr.strip())

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
