from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/release/"
    "promotion-contract.json"
)


def load_contract() -> dict:
    return json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )


def test_promotion_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_promotion_order_is_bounded() -> None:
    contract = load_contract()

    assert contract["promotion_sequence"] == [
        "build",
        "staging",
        "production",
    ]


def test_production_requires_rollback() -> None:
    contract = load_contract()

    assert (
        contract["rollback"][
            "required_for_production"
        ]
        is True
    )


def test_rollback_candidate_must_differ() -> None:
    contract = load_contract()

    assert (
        contract["rollback"][
            "target_must_differ_from_candidate"
        ]
        is True
    )


def test_evidence_paths_are_repository_relative() -> None:
    contract = load_contract()

    for path in contract["evidence"].values():
        assert not path.startswith("/")
        assert ".." not in Path(path).parts
