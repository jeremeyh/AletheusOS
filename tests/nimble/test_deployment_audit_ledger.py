from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger-contract.json"
)

LEDGER_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger.jsonl"
)

WRITER = ROOT / "bin/append_nimble_audit_event.py"

VALIDATOR = ROOT / "bin/validate_nimble_audit_ledger.py"


def test_audit_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_audit_ledger_exists() -> None:
    assert LEDGER_PATH.is_file()


def test_contract_requires_sha256_chain() -> None:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert (
        contract["ledger"]["hash_algorithm"]
        == "sha256"
    )

    assert (
        contract["policy"][
            "tamper_detection_required"
        ]
        is True
    )


def test_empty_ledger_validates() -> None:
    result = subprocess.run(
        [
            "python",
            str(VALIDATOR),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Status: PASS" in result.stdout


def test_event_writer_rejects_sensitive_metadata() -> None:
    result = subprocess.run(
        [
            "python",
            str(WRITER),
            "--event-type",
            "deployment_started",
            "--environment",
            "staging",
            "--release",
            "release-v1",
            "--revision",
            "abc123",
            "--metadata-json",
            '{"token": "forbidden"}',
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0


def test_event_writer_rejects_unknown_event_type() -> None:
    result = subprocess.run(
        [
            "python",
            str(WRITER),
            "--event-type",
            "unknown_event",
            "--environment",
            "staging",
            "--release",
            "release-v1",
            "--revision",
            "abc123",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0


def test_workflows_append_deployment_events() -> None:
    staging = (
        ROOT
        / ".github/workflows/"
        "nimble-staging-promotion.yml"
    ).read_text(encoding="utf-8")

    production = (
        ROOT
        / ".github/workflows/"
        "nimble-production-promotion.yml"
    ).read_text(encoding="utf-8")

    assert "deployment_started" in staging
    assert "deployment_completed" in staging
    assert "health_verified" in staging

    assert "deployment_started" in production
    assert "deployment_completed" in production
    assert "rollback_started" in production
    assert "rollback_completed" in production
    assert "health_verified" in production


def test_audit_helper_exists_and_is_executable() -> None:
    helper = (
        ROOT
        / "scripts/nimble_append_audit_event.sh"
    )

    assert helper.is_file()
    assert helper.stat().st_mode & 0o111


def test_tamper_simulation_detects_modification() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "test_nimble_audit_ledger_tamper.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert (
        "Historical event modification: DETECTED"
        in result.stdout
    )
    assert "Canonical ledger isolation: PASS" in result.stdout
