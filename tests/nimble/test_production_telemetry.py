from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "collect_nimble_production_telemetry.py"


def load_module():
    specification = importlib.util.spec_from_file_location(
        "collect_nimble_production_telemetry",
        MODULE_PATH,
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(specification)

    specification.loader.exec_module(module)

    return module


def test_bundle_budget_matches_production_gate():
    module = load_module()

    assert module.PRIMARY_BUNDLE_LIMIT_BYTES == 500_000


def test_report_paths_are_repository_bounded():
    module = load_module()

    assert module.REPORT_DIRECTORY == (ROOT / "reports" / "nimble")

    assert module.LATEST_JSON.parent == (ROOT / "reports" / "nimble")


def test_bundle_metadata_contract():
    module = load_module()
    metadata = module.collect_bundle_metadata()

    assert "primary_limit_bytes" in metadata
    assert "primary_within_budget" in metadata
    assert "secondary_chunk_count" in metadata
    assert "chunks" in metadata
