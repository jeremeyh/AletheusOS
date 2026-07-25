#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)


REGISTRY_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "deployment-provider-registry.json"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "deployment-provider-registry-latest.json"
)

WORKFLOWS = [
    ROOT
    / ".github/workflows/"
    "nimble-staging-promotion.yml",
    ROOT
    / ".github/workflows/"
    "nimble-production-promotion.yml",
]


def main() -> int:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    registry = json.loads(
        REGISTRY_PATH.read_text(encoding="utf-8")
    )

    providers = registry.get("providers", {})
    default_provider = registry.get("default_provider")

    if default_provider not in providers:
        failures.append(
            "Default deployment provider is not registered."
        )

    for name, provider in providers.items():
        executable_value = provider.get("executable", "")
        executable_relative = Path(executable_value)

        valid_path = (
            not executable_relative.is_absolute()
            and ".." not in executable_relative.parts
        )

        checks.append(
            {
                "check": f"provider-path:{name}",
                "status": "PASS" if valid_path else "FAIL",
            }
        )

        if not valid_path:
            failures.append(
                f"Invalid provider executable path: {name}"
            )
            continue

        executable = ROOT / executable_relative

        if not executable.is_file():
            failures.append(
                f"Missing provider executable: {name}"
            )
        elif not os.access(executable, os.X_OK):
            failures.append(
                f"Provider executable is not executable: {name}"
            )

        if not provider.get("provider_version"):
            failures.append(
                f"Provider version is missing: {name}"
            )

        if not provider.get("supports"):
            failures.append(
                f"Provider actions are missing: {name}"
            )

        if not provider.get("environments"):
            failures.append(
                f"Provider environments are missing: {name}"
            )

    forbidden_tokens = [
        "NIMBLE_DEPLOY_COMMAND",
        "NIMBLE_ROLLBACK_COMMAND",
    ]

    for workflow in WORKFLOWS:
        text = workflow.read_text(encoding="utf-8")

        for token in forbidden_tokens:
            absent = token not in text

            checks.append(
                {
                    "check": (
                        f"forbidden-token:"
                        f"{workflow.name}:{token}"
                    ),
                    "status": (
                        "PASS" if absent else "FAIL"
                    ),
                }
            )

            if not absent:
                failures.append(
                    f"Workflow contains forbidden raw "
                    f"command token: {workflow.name}:{token}"
                )

        if "NIMBLE_DEPLOY_PROVIDER" not in text:
            failures.append(
                f"Workflow does not select a provider: "
                f"{workflow.name}"
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
                "provider_count": len(providers),
                "checks": checks,
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ DEPLOYMENT PROVIDER REGISTRY")
    print("=" * 72)
    print(f"Providers: {len(providers)}")
    print(f"Checks: {len(checks)}")
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
