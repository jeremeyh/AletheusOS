#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

REGISTRY_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "deployment-provider-registry.json"
)

CAPABILITY_CONTRACT_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "provider-capability-contract.json"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "provider-preflight-latest.json"
)

SECRET_NAME_PATTERN = re.compile(
    r"^[A-Z][A-Z0-9_]*$"
)


class ProviderPreflightError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--provider",
        required=True,
    )

    parser.add_argument(
        "--action",
        required=True,
        choices=["deploy", "rollback"],
    )

    parser.add_argument(
        "--environment",
        required=True,
        choices=["staging", "production"],
    )

    parser.add_argument(
        "--mode",
        default=os.environ.get(
            "NIMBLE_DEPLOY_MODE",
            "dry-run",
        ),
        choices=["dry-run", "execute"],
    )

    arguments = parser.parse_args()

    registry = load_json(REGISTRY_PATH)
    contract = load_json(
        CAPABILITY_CONTRACT_PATH
    )

    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    provider = registry.get(
        "providers",
        {},
    ).get(arguments.provider)

    if provider is None:
        failures.append(
            f"Unregistered provider: {arguments.provider}"
        )
    else:
        checks.append(
            {
                "check": "provider-registered",
                "status": "PASS",
            }
        )

    if provider is not None:
        enabled = provider.get("enabled") is True

        checks.append(
            {
                "check": "provider-enabled",
                "status": (
                    "PASS" if enabled else "FAIL"
                ),
            }
        )

        if not enabled:
            failures.append(
                f"Provider is disabled: {arguments.provider}"
            )

        supported_actions = set(
            provider.get("supports", [])
        )

        if arguments.action not in supported_actions:
            failures.append(
                f"Provider does not support action: "
                f"{arguments.action}"
            )

        capabilities = set(
            provider.get("capabilities", [])
        )

        required_capability = arguments.action

        if required_capability not in capabilities:
            failures.append(
                f"Provider lacks required capability: "
                f"{required_capability}"
            )

        allowed_capabilities = set(
            contract["environment_policy"][
                arguments.environment
            ]["allowed_capabilities"]
        )

        if required_capability not in allowed_capabilities:
            failures.append(
                f"Capability {required_capability} is not "
                f"allowed in {arguments.environment}."
            )

        supported_environments = set(
            provider.get("environments", [])
        )

        if (
            arguments.environment
            not in supported_environments
        ):
            failures.append(
                "Provider does not support environment: "
                f"{arguments.environment}"
            )

        version = provider.get(
            "provider_version"
        )

        if not isinstance(version, str) or not version:
            failures.append(
                "Provider version is missing."
            )

        required_secrets_by_environment = (
            provider.get(
                "required_secrets",
                {},
            )
        )

        environment_secrets = (
            required_secrets_by_environment.get(
                arguments.environment
            )
        )

        if not isinstance(environment_secrets, list):
            failures.append(
                "Provider must declare an environment-scoped "
                "required_secrets list."
            )
            environment_secrets = []

        for secret_name in environment_secrets:
            if (
                not isinstance(secret_name, str)
                or not SECRET_NAME_PATTERN.fullmatch(
                    secret_name
                )
            ):
                failures.append(
                    f"Invalid secret declaration: "
                    f"{secret_name!r}"
                )
                continue

            present = bool(
                os.environ.get(secret_name)
            )

            checks.append(
                {
                    "check": (
                        f"required-secret:{secret_name}"
                    ),
                    "status": (
                        "PASS"
                        if present
                        or arguments.mode == "dry-run"
                        else "FAIL"
                    ),
                    "required_in_mode": "execute",
                }
            )

            if (
                arguments.mode == "execute"
                and not present
            ):
                failures.append(
                    f"Required secret is missing: "
                    f"{secret_name}"
                )

        if (
            arguments.environment == "production"
            and arguments.mode == "execute"
            and provider.get(
                "production_execution"
            )
            is not True
        ):
            failures.append(
                f"Provider {arguments.provider} is not "
                "approved for production execution."
            )

        if (
            arguments.environment == "staging"
            and contract["environment_policy"][
                "staging"
            ][
                "production_credentials_forbidden"
            ]
        ):
            production_secret_names = set(
                required_secrets_by_environment.get(
                    "production",
                    [],
                )
            )

            leaked_production_secrets = sorted(
                name
                for name in production_secret_names
                if os.environ.get(name)
            )

            if leaked_production_secrets:
                failures.append(
                    "Production-scoped secrets are present "
                    "during staging execution: "
                    + ", ".join(
                        leaked_production_secrets
                    )
                )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "provider": arguments.provider,
        "action": arguments.action,
        "environment": arguments.environment,
        "mode": arguments.mode,
        "status": status,
        "checks": checks,
        "failures": failures,
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ PROVIDER PREFLIGHT")
    print("=" * 72)
    print(f"Provider: {arguments.provider}")
    print(f"Action: {arguments.action}")
    print(f"Environment: {arguments.environment}")
    print(f"Mode: {arguments.mode}")
    print(f"Status: {status}")
    print(f"Failures: {len(failures)}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
