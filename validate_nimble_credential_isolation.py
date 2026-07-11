#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

REGISTRY_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "deployment-provider-registry.json"
)

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "credential-isolation-contract.json"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "credential-isolation-latest.json"
)

SECRET_PATTERN = re.compile(
    r"^[A-Z][A-Z0-9_]*$"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def fingerprint(
    provider: str,
    environment: str,
    secret_name: str,
    secret_value: str,
    length: int,
) -> str:
    payload = (
        f"{provider}\0"
        f"{environment}\0"
        f"{secret_name}\0"
        f"{secret_value}"
    ).encode("utf-8")

    return hashlib.sha256(payload).hexdigest()[:length]


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--provider",
        required=True,
    )

    parser.add_argument(
        "--environment",
        required=True,
        choices=["staging", "production"],
    )

    parser.add_argument(
        "--mode",
        choices=["dry-run", "execute"],
        default=os.environ.get(
            "NIMBLE_DEPLOY_MODE",
            "dry-run",
        ),
    )

    arguments = parser.parse_args()

    registry = load_json(REGISTRY_PATH)
    contract = load_json(CONTRACT_PATH)

    failures: list[str] = []

    provider = registry.get(
        "providers",
        {},
    ).get(arguments.provider)

    if provider is None:
        failures.append(
            f"Unregistered provider: {arguments.provider}"
        )

        required_for_environment: list[str] = []
        all_environment_secrets: dict[str, list[str]] = {}
    else:
        secret_map = provider.get(
            "required_secrets",
            {},
        )

        if not isinstance(secret_map, dict):
            failures.append(
                "Provider required_secrets must be "
                "an environment-scoped mapping."
            )

            secret_map = {}

        all_environment_secrets = {
            environment: secrets
            for environment, secrets in secret_map.items()
            if isinstance(secrets, list)
        }

        required_for_environment = secret_map.get(
            arguments.environment,
            [],
        )

        if not isinstance(
            required_for_environment,
            list,
        ):
            failures.append(
                "Provider has no valid credential declaration "
                f"for {arguments.environment}."
            )

            required_for_environment = []

    valid_required_names: list[str] = []

    for secret_name in required_for_environment:
        if (
            not isinstance(secret_name, str)
            or not SECRET_PATTERN.fullmatch(secret_name)
        ):
            failures.append(
                "Invalid credential declaration."
            )
            continue

        valid_required_names.append(secret_name)

    foreign_environment_names: set[str] = set()

    for environment, secret_names in (
        all_environment_secrets.items()
    ):
        if environment == arguments.environment:
            continue

        for secret_name in secret_names:
            if isinstance(secret_name, str):
                foreign_environment_names.add(secret_name)

    leaked_foreign_credentials = sorted(
        secret_name
        for secret_name in foreign_environment_names
        if os.environ.get(secret_name)
    )

    if leaked_foreign_credentials:
        failures.append(
            "Credentials scoped to another environment "
            "are present."
        )

    missing_required_credentials = sorted(
        secret_name
        for secret_name in valid_required_names
        if not os.environ.get(secret_name)
    )

    if (
        arguments.mode == "execute"
        and missing_required_credentials
    ):
        failures.append(
            "Required environment credentials are missing."
        )

    truncation = int(
        contract["policy"][
            "fingerprint_truncation"
        ]
    )

    fingerprints = sorted(
        fingerprint(
            arguments.provider,
            arguments.environment,
            secret_name,
            os.environ[secret_name],
            truncation,
        )
        for secret_name in valid_required_names
        if os.environ.get(secret_name)
    )

    if (
        arguments.mode == "execute"
        and len(fingerprints)
        != len(valid_required_names)
    ):
        failures.append(
            "Credential fingerprint set is incomplete."
        )

    rotation_validation = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_credential_rotation.py"
            ),
            "--provider",
            arguments.provider,
            "--environment",
            arguments.environment,
        ],
        cwd=ROOT,
        env=os.environ.copy(),
        capture_output=True,
        text=True,
        check=False,
    )

    if rotation_validation.returncode != 0:
        failures.append(
            "Credential rotation validation failed."
        )

    status = "PASS" if not failures else "FAIL"

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "provider": arguments.provider,
        "environment": arguments.environment,
        "mode": arguments.mode,
        "credential_count": len(
            valid_required_names
        ),
        "credential_fingerprints": fingerprints,
        "status": status,
        "failures": failures,
    }

    serialized_report = json.dumps(
        report,
        indent=2,
        sort_keys=True,
    ) + "\n"

    for secret_name in valid_required_names:
        if secret_name in serialized_report:
            raise RuntimeError(
                "Credential evidence leaked a raw "
                "secret name."
            )

        secret_value = os.environ.get(secret_name)

        if secret_value and secret_value in serialized_report:
            raise RuntimeError(
                "Credential evidence leaked a raw "
                "secret value."
            )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        serialized_report,
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ CREDENTIAL ISOLATION")
    print("=" * 72)
    print(f"Provider: {arguments.provider}")
    print(f"Environment: {arguments.environment}")
    print(f"Mode: {arguments.mode}")
    print(
        "Declared credentials:",
        len(valid_required_names),
    )
    print(
        "Credential fingerprints:",
        len(fingerprints),
    )
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
