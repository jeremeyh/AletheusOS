from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "credential-rotation-contract.json"
)

METADATA_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "credential-metadata.json"
)

REVOCATION_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "credential-revocations.json"
)

VALIDATOR = (
    ROOT
    / "validate_nimble_credential_rotation.py"
)


def test_rotation_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_metadata_registry_exists() -> None:
    assert METADATA_PATH.is_file()


def test_revocation_registry_exists() -> None:
    assert REVOCATION_PATH.is_file()


def test_rotation_thresholds_are_ordered() -> None:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )

    thresholds = contract["thresholds"]

    assert (
        thresholds["critical_before_expiry_days"]
        < thresholds["warning_before_expiry_days"]
        < thresholds["default_max_age_days"]
    )


def test_empty_dry_run_registry_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(VALIDATOR),
            "--provider",
            "dry-run",
            "--environment",
            "staging",
        ],
        cwd=ROOT,
        env=os.environ.copy(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Status: PASS" in result.stdout


def test_contract_forbids_expired_credentials() -> None:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        contract["policy"][
            "expired_credentials_forbidden"
        ]
        is True
    )


def test_contract_requires_rotation_lineage() -> None:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        contract["policy"][
            "lineage_required_after_rotation"
        ]
        is True
    )
