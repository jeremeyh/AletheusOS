#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REGISTRY_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "deployment-provider-registry.json"
)


class ProviderPolicyError(RuntimeError):
    pass


def load_registry() -> dict[str, Any]:
    return json.loads(
        REGISTRY_PATH.read_text(encoding="utf-8")
    )


def resolve_provider(
    registry: dict[str, Any],
    provider_name: str,
    action: str,
    environment: str,
) -> tuple[dict[str, Any], Path]:
    providers = registry.get("providers", {})

    if provider_name not in providers:
        raise ProviderPolicyError(
            f"Unregistered deployment provider: {provider_name}"
        )

    provider = providers[provider_name]

    if provider.get("enabled") is not True:
        raise ProviderPolicyError(
            f"Deployment provider is disabled: {provider_name}"
        )

    if action not in provider.get("supports", []):
        raise ProviderPolicyError(
            f"Provider {provider_name} does not support {action}."
        )

    if environment not in provider.get("environments", []):
        raise ProviderPolicyError(
            f"Provider {provider_name} does not support "
            f"environment {environment}."
        )

    executable_value = provider.get("executable")

    if not isinstance(executable_value, str):
        raise ProviderPolicyError(
            f"Provider {provider_name} has no executable."
        )

    executable_relative = Path(executable_value)

    if executable_relative.is_absolute():
        raise ProviderPolicyError(
            "Absolute provider executable paths are forbidden."
        )

    if ".." in executable_relative.parts:
        raise ProviderPolicyError(
            "Provider executable path traversal is forbidden."
        )

    executable = (ROOT / executable_relative).resolve()

    provider_root = (
        ROOT / "scripts/nimble_providers"
    ).resolve()

    if provider_root not in executable.parents:
        raise ProviderPolicyError(
            "Provider executable must remain inside "
            "scripts/nimble_providers."
        )

    if not executable.is_file():
        raise ProviderPolicyError(
            f"Provider executable is missing: {executable_relative}"
        )

    if not os.access(executable, os.X_OK):
        raise ProviderPolicyError(
            f"Provider executable is not executable: "
            f"{executable_relative}"
        )

    if (
        environment == "production"
        and os.environ.get("NIMBLE_DEPLOY_MODE") == "execute"
        and provider.get("production_execution") is not True
    ):
        raise ProviderPolicyError(
            f"Provider {provider_name} is not approved for "
            "production execution."
        )

    return provider, executable


def main() -> int:
    parser = argparse.ArgumentParser()

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
        "--provider",
        default=os.environ.get("NIMBLE_DEPLOY_PROVIDER"),
    )

    arguments = parser.parse_args()

    registry = load_registry()

    provider_name = (
        arguments.provider
        or registry.get("default_provider")
    )

    if not isinstance(provider_name, str):
        raise ProviderPolicyError(
            "No deployment provider was selected."
        )

    provider, executable = resolve_provider(
        registry,
        provider_name,
        arguments.action,
        arguments.environment,
    )

    preflight = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_provider_preflight.py"
            ),
            "--provider",
            provider_name,
            "--action",
            arguments.action,
            "--environment",
            arguments.environment,
            "--mode",
            os.environ.get(
                "NIMBLE_DEPLOY_MODE",
                "dry-run",
            ),
        ],
        cwd=ROOT,
        env=os.environ.copy(),
        check=False,
    )

    if preflight.returncode != 0:
        raise ProviderPolicyError(
            "Provider preflight validation failed."
        )

    child_environment = {
        **os.environ,
        "NIMBLE_PROVIDER_NAME": provider_name,
        "NIMBLE_PROVIDER_VERSION": str(
            provider["provider_version"]
        ),
        "NIMBLE_PROVIDER_ACTION": arguments.action,
        "NIMBLE_ENVIRONMENT": arguments.environment,
    }

    print("=" * 72)
    print("NIMBLE™ DEPLOYMENT PROVIDER DISPATCH")
    print("=" * 72)
    print(f"Provider: {provider_name}")
    print(
        f"Provider version: "
        f"{provider['provider_version']}"
    )
    print(f"Action: {arguments.action}")
    print(f"Environment: {arguments.environment}")
    print(
        "Executable:",
        executable.relative_to(ROOT),
    )

    result = subprocess.run(
        [str(executable)],
        cwd=ROOT,
        env=child_environment,
        check=False,
    )

    return result.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProviderPolicyError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1) from None
