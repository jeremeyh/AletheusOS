from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

GENERATOR = ROOT / "generate_nimble_dependency_manifest.py"

VALIDATOR = ROOT / "validate_nimble_dependency_manifest.py"


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(
        name,
        path,
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    return module


def test_manifest_paths_are_canonical():
    module = load_module(
        "dependency_manifest_generator",
        GENERATOR,
    )

    assert module.MANIFEST == (
        ROOT / "nimble" / "governance" / "supply-chain" / "dependency-manifest.json"
    )


def test_npm_inventory_contract():
    module = load_module(
        "dependency_manifest_generator",
        GENERATOR,
    )

    inventory = module.collect_npm_dependencies()

    assert "package_lock_sha256" in inventory
    assert "resolved_package_count" in inventory
    assert "resolved_packages" in inventory


def test_validator_requires_runtime_and_dependency_data():
    module = load_module(
        "dependency_manifest_validator",
        VALIDATOR,
    )

    assert {
        "runtime",
        "npm",
        "python",
    } <= module.REQUIRED_TOP_LEVEL_KEYS
