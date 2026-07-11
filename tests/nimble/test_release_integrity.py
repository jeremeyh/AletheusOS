from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/release/"
    "release-integrity-contract.json"
)


def load_contract() -> dict:
    return json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )


def test_release_integrity_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_release_integrity_uses_sha256() -> None:
    contract = load_contract()

    assert contract["hash_algorithm"] == "sha256"


def test_release_manifest_has_checksum_sidecar() -> None:
    contract = load_contract()

    assert (
        contract["manifest"]["checksum_path"]
        == "reports/nimble/"
        "nimble-release-manifest.sha256"
    )


def test_required_subjects_are_repository_relative() -> None:
    contract = load_contract()

    for subject in contract["required_subjects"]:
        assert not subject.startswith("/")
        assert ".." not in Path(subject).parts


def test_attestation_is_sigstore_backed() -> None:
    contract = load_contract()

    assert (
        contract["attestation"]["provider"]
        == "github-artifact-attestations"
    )

    assert (
        contract["attestation"]["action"]
        == "actions/attest@v4"
    )

    assert (
        contract["attestation"]["sigstore_backed"]
        is True
    )
