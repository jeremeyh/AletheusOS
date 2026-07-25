#!/usr/bin/env python3

from __future__ import annotations

import json
import re
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

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "provider-capability-contract.json"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "provider-capability-validation-latest.json"
)

SECRET_NAME_PATTERN = re.compile(
    r"^[A-Z][A-Z0-9_]*$"
)


def main() -> int:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    registry = json.loads(
        REGISTRY_PATH.read_text(
            encoding="utf-8"
        )
    )

    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )

    known_capabilities = set(
        contract["capabilities"]
    )

    for provider_name, provider in (
        registry.get("providers", {}).items()
    ):
        capabilities = provider.get(
            "capabilities"
        )

        valid_capability_list = (
            isinstance(capabilities, list)
            and bool(capabilities)
        )

        checks.append(
            {
                "check": (
                    f"capability-list:{provider_name}"
                ),
                "status": (
                    "PASS"
                    if valid_capability_list
                    else "FAIL"
                ),
            }
        )

        if not valid_capability_list:
            failures.append(
                f"Provider has no declared capabilities: "
                f"{provider_name}"
            )
            continue

        unknown = sorted(
            set(capabilities)
            - known_capabilities
        )

        if unknown:
            failures.append(
                f"Provider {provider_name} declares "
                "unknown capabilities: "
                + ", ".join(unknown)
            )

        actions = set(
            provider.get("supports", [])
        )

        missing_action_capabilities = sorted(
            actions - set(capabilities)
        )

        if missing_action_capabilities:
            failures.append(
                f"Provider {provider_name} lacks "
                "capabilities matching supported actions: "
                + ", ".join(
                    missing_action_capabilities
                )
            )

        secret_map = provider.get(
            "required_secrets"
        )

        if not isinstance(secret_map, dict):
            failures.append(
                f"Provider {provider_name} must declare "
                "required_secrets by environment."
            )
            continue

        for environment in provider.get(
            "environments",
            [],
        ):
            declared = secret_map.get(
                environment
            )

            if not isinstance(declared, list):
                failures.append(
                    f"Provider {provider_name} has no "
                    f"secret declaration for {environment}."
                )
                continue

            for secret_name in declared:
                if (
                    not isinstance(secret_name, str)
                    or not SECRET_NAME_PATTERN.fullmatch(
                        secret_name
                    )
                ):
                    failures.append(
                        f"Invalid secret name for "
                        f"{provider_name}: "
                        f"{secret_name!r}"
                    )

        serialized = json.dumps(provider)

        suspicious_values = [
            "password=",
            "token=",
            "secret=",
            "apikey=",
            "api_key=",
        ]

        for token in suspicious_values:
            if token in serialized.lower():
                failures.append(
                    f"Provider registry may contain "
                    f"a plaintext secret: "
                    f"{provider_name}:{token}"
                )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

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
    print("NIMBLE™ PROVIDER CAPABILITY GOVERNANCE")
    print("=" * 72)
    print(
        "Providers:",
        len(registry.get("providers", {})),
    )
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
