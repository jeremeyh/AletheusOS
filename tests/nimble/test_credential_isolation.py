from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT / "nimble/governance/environments/credential-isolation-contract.json"
)

VALIDATOR = ROOT / "validate_nimble_credential_isolation.py"

REPORT_PATH = ROOT / "reports/nimble/credential-isolation-latest.json"


def run_validator(
    environment: str,
    mode: str = "dry-run",
    extra_environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    runtime_environment = {
        **os.environ,
        **(extra_environment or {}),
    }

    return subprocess.run(
        [
            "python",
            str(VALIDATOR),
            "--provider",
            "dry-run",
            "--environment",
            environment,
            "--mode",
            mode,
        ],
        cwd=ROOT,
        env=runtime_environment,
        capture_output=True,
        text=True,
        check=False,
    )


def test_credential_isolation_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_contract_uses_sha256_fingerprints() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["policy"]["fingerprint_algorithm"] == "sha256"


def test_dry_run_passes_without_credentials() -> None:
    result = run_validator("staging")

    assert result.returncode == 0
    assert "Status: PASS" in result.stdout


def test_public_evidence_contains_no_raw_secret_names() -> None:
    result = run_validator("staging")

    assert result.returncode == 0

    report_text = REPORT_PATH.read_text(encoding="utf-8")

    assert "NIMBLE_STAGING_TOKEN" not in report_text
    assert "NIMBLE_PRODUCTION_TOKEN" not in report_text


def test_public_evidence_contains_no_raw_secret_values() -> None:
    secret_value = "super-sensitive-example-value"

    result = run_validator(
        "staging",
        extra_environment={
            "UNDECLARED_TEST_SECRET": secret_value,
        },
    )

    assert result.returncode == 0

    report_text = REPORT_PATH.read_text(encoding="utf-8")

    assert secret_value not in report_text


def test_unregistered_provider_fails_closed() -> None:
    result = subprocess.run(
        [
            "python",
            str(VALIDATOR),
            "--provider",
            "unknown-provider",
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

    assert result.returncode != 0
    assert "Unregistered provider" in result.stdout
