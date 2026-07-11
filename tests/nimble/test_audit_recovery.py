from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/audit/recovery/"
    "audit-recovery-contract.json"
)

PLANNER = (
    ROOT
    / "plan_nimble_audit_recovery.py"
)

CONTRACT_VALIDATOR = (
    ROOT
    / "validate_nimble_audit_recovery_contract.py"
)


def load_contract() -> dict:
    return json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )


def test_recovery_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_recovery_defaults_to_plan_only() -> None:
    assert load_contract()["mode"] == "plan_only"


def test_automatic_mutation_is_forbidden() -> None:
    contract = load_contract()

    assert (
        contract["policy"][
            "automatic_ledger_mutation_forbidden"
        ]
        is True
    )


def test_snapshot_is_required_before_apply() -> None:
    contract = load_contract()

    assert (
        contract["policy"][
            "pre_recovery_snapshot_required_before_apply"
        ]
        is True
    )


def test_contract_validator_passes() -> None:
    result = subprocess.run(
        ["python", str(CONTRACT_VALIDATOR)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Status: PASS" in result.stdout


def test_healthy_ledger_produces_no_action_plan() -> None:
    result = subprocess.run(
        ["python", str(PLANNER)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Classification: healthy" in result.stdout
    assert "Recommended action: none" in result.stdout
    assert "Mutation performed: False" in result.stdout


def test_trusted_recovery_source_contract() -> None:
    contract = load_contract()
    source = contract["trusted_recovery_source"]

    assert source["hash_algorithm"] == "sha256"

    assert (
        source["requirements"][
            "canonical_ledger_mutation_forbidden"
        ]
        is True
    )


def test_recovery_source_generator_and_validator() -> None:
    generator = (
        ROOT
        / "create_nimble_audit_recovery_source.py"
    )

    validator = (
        ROOT
        / "validate_nimble_audit_recovery_source.py"
    )

    generated = subprocess.run(
        ["python", str(generator)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert generated.returncode == 0

    validated = subprocess.run(
        [
            "python",
            str(validator),
            "--no-write",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert validated.returncode == 0
    assert "Status: PASS" in validated.stdout
    assert (
        "Canonical ledger mutation: False"
        in validated.stdout
    )


def test_isolated_recovery_simulation() -> None:
    simulation = (
        ROOT
        / "test_nimble_audit_recovery_simulation.py"
    )

    result = subprocess.run(
        ["python", str(simulation)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Separate reconstruction: PASS" in result.stdout
    assert (
        "Automatic canonical mutation: BLOCKED"
        in result.stdout
    )
    assert (
        "Canonical ledger isolation: PASS"
        in result.stdout
    )



def test_isolated_recovery_apply_simulation() -> None:
    simulation = (
        ROOT
        / "test_nimble_audit_recovery_apply_simulation.py"
    )

    result = subprocess.run(
        ["python", str(simulation)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )

    assert (
        "Atomic ledger replacement: PASS"
        in result.stdout
    )

    assert (
        "Recovery provenance append: PASS"
        in result.stdout
    )

    assert (
        "Validation-failure rollback: PASS"
        in result.stdout
    )

    assert (
        "Canonical ledger isolation: PASS"
        in result.stdout
    )
