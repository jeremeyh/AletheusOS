#!/usr/bin/env python3
"""
Compatibility entry point for the Nimble attested release validator.
"""

from pathlib import Path

from tools.validation.nimble import validate_nimble_attested_release as _impl


def _find_repo_root() -> Path:
    probe = Path(__file__).resolve().parent
    while True:
        if (probe / "pyproject.toml").is_file():
            return probe
        if probe.parent == probe:
            raise RuntimeError("Unable to locate repository root.")
        probe = probe.parent


ROOT = _find_repo_root()

WORKFLOW = (
    ROOT
    / ".github"
    / "workflows"
    / "nimble-attested-release.yml"
)

REQUIRED_MARKERS = tuple(
    dict.fromkeys(
        (
            *getattr(_impl, "REQUIRED_MARKERS", ()),
            "Attestation commit matches tagged commit",
        )
    )
)

for _name in dir(_impl):
    if _name.startswith("_"):
        continue
    if _name in {"WORKFLOW", "REQUIRED_MARKERS"}:
        continue
    globals()[_name] = getattr(_impl, _name)
