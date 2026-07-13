#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REACT = (
    ROOT
    / "nimble/packages/react/src/instrumentation"
)

SHELL = (
    ROOT
    / "nimble/apps/platform-shell"
)

REPORT = (
    ROOT
    / "reports/nimble/experience/"
    "instrumentation-preview-validation-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required_react = [
        "canonical.ts",
        "context.tsx",
        "contracts.ts",
        "fixtures.ts",
        "formatting.ts",
        "hooks.ts",
        "index.ts",
        "registry.ts",
        "validation.ts",
    ]

    required_shell = [
        "instrumentation.html",
        "vite.instrumentation.config.ts",
        "src/instrumentation-preview.tsx",
        "src/nimble/showcase/IntelligenceInstrumentationShowcase.tsx",
        "src/nimble/showcase/instrumentation-preview.css",
    ]

    for relative in required_react:
        if not (
            REACT / relative
        ).is_file():
            failures.append(
                "Missing instrumentation framework file: "
                + relative
            )

    for relative in required_shell:
        if not (
            SHELL / relative
        ).is_file():
            failures.append(
                "Missing instrumentation preview file: "
                + relative
            )

    combined = "\n".join(
        path.read_text(
            encoding="utf-8"
        )
        for root in [
            REACT,
            SHELL
            / "src/nimble/showcase",
        ]
        if root.exists()
        for path in root.rglob("*")
        if (
            path.is_file()
            and path.suffix
            in {
                ".ts",
                ".tsx",
                ".css",
            }
        )
    )

    concepts = [
        "Aletheus Index™",
        "THORᵡ",
        "Evidence Engine™",
        "Knowledge Engine™",
        "Reason Engine™",
        "Memory Engine™",
        "Bias Engine™",
        "Risk Engine™",
        "Predictive Engine™",
        "Individual Engine Grades",
        "InstrumentationRegistry",
        "Reserved instrument cannot be renamed",
        "prefers-reduced-motion",
    ]

    for concept in concepts:
        if concept not in combined:
            failures.append(
                "Missing instrumentation concept: "
                + concept
            )

    commands = [
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-react",
        ],
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-shell",
        ],
        [
            "npm",
            "run",
            "build:instrumentation",
            "--workspace",
            "@aletheus/nimble-shell",
        ],
    ]

    results: list[
        dict[str, object]
    ] = []

    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT / "nimble",
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )

        results.append(
            {
                "command":
                    " ".join(command),

                "returncode":
                    result.returncode,

                "stdout":
                    result.stdout.strip(),

                "stderr":
                    result.stderr.strip(),
            }
        )

        if result.returncode != 0:
            failures.append(
                "Command failed: "
                + " ".join(command)
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
                "schema_version":
                    "1.0",

                "generated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                "status":
                    status,

                "failures":
                    failures,

                "commands":
                    results,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(
        "NIMBLE™ INTELLIGENCE INSTRUMENTATION PREVIEW"
    )
    print("=" * 72)
    print(
        f"Failures: {len(failures)}"
    )
    print(
        f"Status: {status}"
    )
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    for failure in failures:
        print(
            f"- {failure}"
        )

    if failures:
        for result in results:
            if result[
                "returncode"
            ] != 0:
                print()
                print(
                    result["command"]
                )
                print(
                    result["stdout"]
                )
                print(
                    result["stderr"]
                )

    return (
        0
        if status == "PASS"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
