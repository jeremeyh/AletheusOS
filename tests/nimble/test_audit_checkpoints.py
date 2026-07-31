from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = ROOT / "nimble/governance/audit/audit-checkpoint-contract.json"

CHECKPOINT_DIRECTORY = ROOT / "nimble/governance/audit/checkpoints"

VALIDATOR = ROOT / "bin/validate_nimble_audit_checkpoints.py"


def test_checkpoint_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_checkpoint_directory_exists() -> None:
    assert CHECKPOINT_DIRECTORY.is_dir()


def test_checkpoint_contract_uses_sha256() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["checkpoint"]["hash_algorithm"] == "sha256"


def test_contract_requires_truncation_detection() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["policy"]["ledger_truncation_detection_required"] is True


def test_contract_requires_rollback_detection() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["policy"]["ledger_rollback_detection_required"] is True


def test_empty_checkpoint_chain_validates() -> None:
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


def test_checkpoint_tamper_simulation() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "tests"
                / "nimble"
                / "audit"
                / "test_nimble_audit_checkpoint_tamper.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        f"Checkpoint tamper simulation failed.\n\n"
        f"STDOUT:\n{result.stdout}\n\n"
        f"STDERR:\n{result.stderr}"
    )
    assert "Ledger truncation: DETECTED" in result.stdout
    assert "Ledger rollback/replacement: DETECTED" in result.stdout
    assert "Canonical checkpoint isolation: PASS" in result.stdout
