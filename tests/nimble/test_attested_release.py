from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = (
    ROOT
    / "validate_nimble_attested_release.py"
)


def load_module():
    specification = (
        importlib.util.spec_from_file_location(
            "validate_nimble_attested_release",
            MODULE_PATH,
        )
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(
        specification
    )

    specification.loader.exec_module(module)

    return module


def test_release_workflow_path_is_canonical():
    module = load_module()

    assert module.WORKFLOW == (
        ROOT
        / ".github"
        / "workflows"
        / "nimble-attested-release.yml"
    )


def test_release_contract_requires_attestation():
    module = load_module()

    assert (
        "python validate_nimble_release_attestation.py"
        in module.REQUIRED_MARKERS
    )


def test_release_contract_requires_tag_binding():
    module = load_module()

    assert (
        "Attestation commit matches tagged commit"
        in module.REQUIRED_MARKERS
    )
