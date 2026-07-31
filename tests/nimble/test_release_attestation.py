from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

GENERATOR = ROOT / "generate_nimble_release_attestation.py"

VALIDATOR = ROOT / "validate_nimble_release_attestation.py"


def load_module(
    name: str,
    path: Path,
):
    specification = importlib.util.spec_from_file_location(
        name,
        path,
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(specification)

    specification.loader.exec_module(module)

    return module


def test_canonical_digest_is_deterministic():
    module = load_module(
        "generate_attestation",
        GENERATOR,
    )

    first = module.canonical_digest(
        {
            "b": 2,
            "a": 1,
        }
    )

    second = module.canonical_digest(
        {
            "a": 1,
            "b": 2,
        }
    )

    assert first == second


def test_hash_directory_contract():
    module = load_module(
        "generate_attestation",
        GENERATOR,
    )

    result = module.hash_directory(ROOT / "nimble" / "apps" / "platform-shell" / "dist")

    assert "files" in result
    assert "file_count" in result
    assert "aggregate_sha256" in result


def test_validator_requires_digest():
    module = load_module(
        "validate_attestation",
        VALIDATOR,
    )

    assert "attestation_sha256" in module.REQUIRED_TOP_LEVEL_KEYS
