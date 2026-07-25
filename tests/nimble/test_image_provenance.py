from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/deployment/"
    "image-provenance-contract.json"
)

DOCKERFILE_PATH = ROOT / "Dockerfile.nimble"


def test_image_provenance_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_dockerfile_contains_required_oci_labels() -> None:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    dockerfile = DOCKERFILE_PATH.read_text(
        encoding="utf-8",
    )

    for label in contract["image"][
        "required_oci_labels"
    ]:
        assert label in dockerfile


def test_provenance_contract_requires_digest() -> None:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    assert (
        contract["provenance"][
            "digest_algorithm"
        ]
        == "sha256"
    )

    assert (
        contract["provenance"][
            "digest_required_in_ci"
        ]
        is True
    )


def test_provenance_contract_requires_sbom() -> None:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    assert contract["sbom"]["required_in_ci"] is True
    assert contract["sbom"]["format"] == "spdx-json"
    assert contract["sbom"]["generator"] == "syft"
