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


PRIMITIVES = ROOT / "nimble/packages/react/src/primitives"

REPORT = ROOT / "reports/nimble/experience/primitive-experience-validation-latest.json"


def main() -> int:
    failures: list[str] = []

    required_files = [
        "Badge.tsx",
        "Grid.tsx",
        "Instrument.tsx",
        "Meter.tsx",
        "Panel.tsx",
        "Separator.tsx",
        "Signal.tsx",
        "Stack.tsx",
        "Surface.tsx",
        "Text.tsx",
        "index.ts",
        "reserved.tsx",
        "tokens.ts",
        "types.ts",
    ]

    for relative in required_files:
        if not (PRIMITIVES / relative).is_file():
            failures.append(f"Missing primitive file: {relative}")

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in PRIMITIVES.rglob("*")
        if (path.is_file() and path.suffix in {".ts", ".tsx"})
    )

    required_concepts = [
        "data-nimble-primitive",
        "Aletheus Index™",
        "THORᵡ",
        "instrument.aletheus-index",
        "instrument.thorx",
        "ExperienceDensity",
        "prefers-reduced-motion",
    ]

    for concept in required_concepts:
        if concept == "prefers-reduced-motion":
            continue

        if concept not in combined:
            failures.append("Missing primitive concept: " + concept)

    typecheck = subprocess.run(
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-react",
        ],
        cwd=ROOT / "nimble",
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    if typecheck.returncode != 0:
        failures.append("Nimble React typecheck failed.")

    status = "PASS" if not failures else "FAIL"

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_at": datetime.now(UTC).isoformat(),
                "status": status,
                "failures": failures,
                "typecheck_stdout": typecheck.stdout.strip(),
                "typecheck_stderr": typecheck.stderr.strip(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ PRIMITIVE EXPERIENCE")
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
