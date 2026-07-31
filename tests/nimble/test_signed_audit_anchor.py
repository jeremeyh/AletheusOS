from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = ROOT / "nimble/governance/audit/signed-audit-anchor-contract.json"

GENERATOR = ROOT / "bin/create_nimble_signed_audit_anchor.py"

VALIDATOR = ROOT / "bin/validate_nimble_signed_audit_anchor.py"


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_signed_anchor_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_signed_anchor_uses_sha256() -> None:
    contract = load_contract()

    assert contract["anchor"]["hash_algorithm"] == "sha256"


def test_signed_anchor_is_keyless() -> None:
    contract = load_contract()

    assert contract["signing"]["keyless"] is True
    assert contract["signing"]["sigstore_backed"] is True


def test_signed_anchor_binds_checkpoint() -> None:
    contract = load_contract()

    assert contract["subject"]["checkpoint_hash_binding_required"] is True

    assert contract["subject"]["ledger_head_binding_required"] is True


def test_anchor_generator_runs() -> None:
    result = subprocess.run(
        ["python", str(GENERATOR)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0


def test_generated_anchor_validates() -> None:
    result = subprocess.run(
        ["python", str(VALIDATOR)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Status: PASS" in result.stdout


def test_signing_workflow_exists() -> None:
    workflow = ROOT / ".github/workflows/nimble-audit-anchor.yml"

    assert workflow.is_file()


def test_signing_workflow_uses_first_party_attestation() -> None:
    workflow = (ROOT / ".github/workflows/nimble-audit-anchor.yml").read_text(
        encoding="utf-8"
    )

    assert "uses: actions/attest@v4" in workflow
    assert "id-token: write" in workflow
    assert "attestations: write" in workflow


def test_signing_workflow_verifies_signer_identity() -> None:
    workflow = (ROOT / ".github/workflows/nimble-audit-anchor.yml").read_text(
        encoding="utf-8"
    )

    assert "gh attestation verify" in workflow
    assert "--repo" in workflow
    assert "--signer-workflow" in workflow


def test_signing_workflow_exists() -> None:
    workflow = ROOT / ".github/workflows/nimble-audit-anchor.yml"

    assert workflow.is_file()


def test_signing_workflow_uses_first_party_attestation() -> None:
    workflow = (ROOT / ".github/workflows/nimble-audit-anchor.yml").read_text(
        encoding="utf-8"
    )

    assert "uses: actions/attest@v4" in workflow
    assert "id-token: write" in workflow
    assert "attestations: write" in workflow


def test_signing_workflow_verifies_signer_identity() -> None:
    workflow = (ROOT / ".github/workflows/nimble-audit-anchor.yml").read_text(
        encoding="utf-8"
    )

    assert "gh attestation verify" in workflow
    assert "--repo" in workflow
    assert "--signer-workflow" in workflow
