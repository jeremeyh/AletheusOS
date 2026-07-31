#!/usr/bin/env python3

from __future__ import annotations

import json
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


CONTRACT_PATH = (
    ROOT / "nimble/governance/environments/credential-isolation-contract.json"
)

REGISTRY_PATH = (
    ROOT / "nimble/governance/environments/deployment-provider-registry.json"
)

REPORT_PATH = ROOT / "reports/nimble/credential-contract-validation-latest.json"


def main() -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    failures: list[str] = []

    policy = contract.get("policy", {})

    required_true_policies = [
        "provider_binding_required",
        "environment_binding_required",
        "cross_environment_credentials_forbidden",
        "raw_secret_values_forbidden_in_evidence",
        "raw_secret_names_forbidden_in_public_evidence",
        "credential_fingerprints_required_in_execute_mode",
        "fail_closed",
    ]

    for name in required_true_policies:
        if policy.get(name) is not True:
            failures.append(f"Credential policy must be true: {name}")

    if policy.get("fingerprint_algorithm") != "sha256":
        failures.append("Credential fingerprint algorithm must be sha256.")

    truncation = policy.get("fingerprint_truncation")

    if not isinstance(truncation, int) or truncation < 12:
        failures.append(
            "Credential fingerprint truncation must be at least 12 characters."
        )

    for provider_name, provider in registry.get("providers", {}).items():
        secret_map = provider.get("required_secrets")

        if not isinstance(secret_map, dict):
            failures.append(
                f"Provider lacks environment-scoped credentials: {provider_name}"
            )
            continue

        for environment in provider.get(
            "environments",
            [],
        ):
            if environment not in secret_map:
                failures.append(
                    f"Provider {provider_name} lacks "
                    f"credential scope for {environment}."
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
                "generated_at": datetime.now(UTC).isoformat(),
                "status": status,
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ CREDENTIAL CONTRACT")
    print("=" * 72)
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
