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


EXPERIENCE_ROOT = (
    ROOT
    / "nimble/packages/core/src/experience"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/experience/"
    "experience-core-validation-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required_files = [
        "contracts.ts",
        "index.ts",
        "tokens/index.ts",
        "tokens/instrumentation.ts",
        "tokens/primitives.ts",
        "tokens/registry.ts",
        "tokens/semantic.ts",
        "tokens/validator.ts",
        "theme/contracts.ts",
        "theme/index.ts",
        "theme/registry.ts",
        "theme/themes.ts",
    ]

    for relative in required_files:
        path = EXPERIENCE_ROOT / relative

        if not path.is_file():
            failures.append(
                f"Missing Experience Core file: {relative}"
            )

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in EXPERIENCE_ROOT.rglob("*.ts")
    )

    required_concepts = [
        "Aletheus Index™",
        "thorx",
        "instrumentation.engine.evidence",
        "instrumentation.engine.knowledge",
        "instrumentation.engine.bias",
        "instrumentation.engine.risk",
        "instrumentation.engine.predictive",
        "aletheus.instrumentation",
        "class TokenRegistry",
        "class ThemeRegistry",
    ]

    for concept in required_concepts:
        if concept not in combined:
            failures.append(
                f"Missing Experience Core concept: {concept}"
            )

    typecheck = subprocess.run(
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-core",
        ],
        cwd=ROOT / "nimble",
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )

    if typecheck.returncode != 0:
        failures.append(
            "Nimble Core TypeScript typecheck failed."
        )

    status = "PASS" if not failures else "FAIL"

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_at": datetime.now(
                    UTC
                ).isoformat(),
                "status": status,
                "failures": failures,
                "typecheck_stdout": (
                    typecheck.stdout.strip()
                ),
                "typecheck_stderr": (
                    typecheck.stderr.strip()
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ EXPERIENCE CORE")
    print("=" * 72)
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    if typecheck.stdout.strip():
        print(typecheck.stdout.strip())

    if typecheck.stderr.strip():
        print(typecheck.stderr.strip())

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
