from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

VALIDATOR = (
    ROOT
    / "validate_nimble_container_contract.py"
)

CONTRACT = (
    ROOT
    / "nimble"
    / "governance"
    / "deployment"
    / "container-contract.json"
)


def load_module():
    specification = (
        importlib.util.spec_from_file_location(
            "container_contract_validator",
            VALIDATOR,
        )
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(
        specification
    )

    specification.loader.exec_module(module)

    return module


def test_container_contract_is_non_root():
    contract = json.loads(
        CONTRACT.read_text(encoding="utf-8")
    )

    assert contract["runtime"]["user"] != "root"


def test_container_contract_requires_hardening():
    contract = json.loads(
        CONTRACT.read_text(encoding="utf-8")
    )

    runtime = contract["runtime"]

    assert runtime[
        "read_only_root_filesystem"
    ] is True

    assert runtime[
        "drop_all_capabilities"
    ] is True

    assert runtime[
        "no_new_privileges"
    ] is True


def test_validator_requires_probe_markers():
    module = load_module()

    assert "/healthz" in (
        module.REQUIRED_COMPOSE_MARKERS
    )

    assert "/readyz" in (
        module.REQUIRED_COMPOSE_MARKERS
    )
