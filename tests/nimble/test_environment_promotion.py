from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "environment-promotion-contract.json"
)


def load_contract() -> dict:
    return json.loads(
        CONTRACT_PATH.read_text(encoding="utf-8")
    )


def test_environment_contract_exists() -> None:
    assert CONTRACT_PATH.is_file()


def test_staging_precedes_production() -> None:
    contract = load_contract()

    assert (
        contract["promotion_policy"][
            "staging_before_production"
        ]
        is True
    )


def test_production_requires_approval() -> None:
    contract = load_contract()

    assert (
        contract["environments"]["production"][
            "requires_manual_approval"
        ]
        is True
    )


def test_production_requires_rollback() -> None:
    contract = load_contract()

    assert (
        contract["environments"]["production"][
            "rollback_required"
        ]
        is True
    )


def test_health_checks_are_required() -> None:
    contract = load_contract()

    assert (
        contract["environments"]["staging"][
            "health_probe_required"
        ]
        is True
    )

    assert (
        contract["environments"]["production"][
            "health_probe_required"
        ]
        is True
    )


def test_evidence_paths_are_repository_relative() -> None:
    contract = load_contract()

    for path in contract["evidence"].values():
        candidate = Path(path)

        assert not candidate.is_absolute()
        assert ".." not in candidate.parts
