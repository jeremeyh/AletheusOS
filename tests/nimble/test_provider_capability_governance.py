from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

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

PREFLIGHT = (
    ROOT
    / "validate_nimble_provider_preflight.py"
)


def load_json(path: Path) -> dict:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def test_capability_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_all_provider_capabilities_are_known() -> None:
    registry = load_json(REGISTRY_PATH)
    contract = load_json(CONTRACT_PATH)

    known = set(contract["capabilities"])

    for provider in registry["providers"].values():
        assert set(provider["capabilities"]) <= known


def test_supported_actions_have_capabilities() -> None:
    registry = load_json(REGISTRY_PATH)

    for provider in registry["providers"].values():
        assert set(provider["supports"]) <= set(
            provider["capabilities"]
        )


def test_required_secrets_are_environment_scoped() -> None:
    registry = load_json(REGISTRY_PATH)

    for provider in registry["providers"].values():
        for environment in provider["environments"]:
            assert environment in provider[
                "required_secrets"
            ]

            assert isinstance(
                provider["required_secrets"][
                    environment
                ],
                list,
            )


def test_dry_run_preflight_passes_without_secrets() -> None:
    result = subprocess.run(
        [
            "python",
            str(PREFLIGHT),
            "--provider",
            "dry-run",
            "--action",
            "deploy",
            "--environment",
            "staging",
            "--mode",
            "dry-run",
        ],
        cwd=ROOT,
        env=os.environ.copy(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Status: PASS" in result.stdout


def test_dry_run_provider_cannot_execute_production() -> None:
    result = subprocess.run(
        [
            "python",
            str(PREFLIGHT),
            "--provider",
            "dry-run",
            "--action",
            "deploy",
            "--environment",
            "production",
            "--mode",
            "execute",
        ],
        cwd=ROOT,
        env=os.environ.copy(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0

    assert (
        "not approved for production execution"
        in result.stdout
    )
