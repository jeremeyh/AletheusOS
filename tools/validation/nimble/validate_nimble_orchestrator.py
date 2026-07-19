#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REPORT = (
    ROOT
    / "reports/nimble/orchestrator/"
    "build-state-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required = [
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
            failures.append(
                f"Missing orchestrator file: {relative}"
            )

    result = subprocess.run(
        [
            "python",
            "-m",
            "nimble.orchestrator",
            "--root",
            str(ROOT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    if result.returncode != 0:
        failures.append(
            "Nimble Build Orchestrator execution failed."
        )

    if not REPORT.is_file():
        failures.append(
            "Orchestrator state report was not generated."
        )
        report = {}
    else:
        report = json.loads(
            REPORT.read_text(
                encoding="utf-8"
            )
        )

        if (
            report.get("schema_version")
            != "1.0"
        ):
            failures.append(
                "Invalid orchestrator report schema."
            )

        capability_ids = {
            item["capability_id"]
            for item in report.get(
                "capabilities",
                [],
            )
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
                "Missing orchestrator capabilities: "
                + ", ".join(sorted(missing))
            )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

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
