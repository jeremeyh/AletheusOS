from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PROMOTION_MODULE_PATH = (
    ROOT
    / "promote_nimble_performance_baseline.py"
)

VALIDATOR_MODULE_PATH = (
    ROOT
    / "validate_nimble_baseline_governance.py"
)


def load_module(
    name: str,
    path: Path,
):
    specification = (
        importlib.util.spec_from_file_location(
            name,
            path,
        )
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(
        specification
    )

    specification.loader.exec_module(module)

    return module


def test_promotion_paths_are_repository_bounded():
    module = load_module(
        "promote_nimble_performance_baseline",
        PROMOTION_MODULE_PATH,
    )

    assert module.CURRENT_BASELINE == (
        ROOT
        / "nimble"
        / "governance"
        / "performance-baseline.json"
    )

    assert module.BASELINE_HISTORY.parent == (
        ROOT
        / "nimble"
        / "governance"
    )


def test_baseline_metrics_are_derived_from_telemetry():
    module = load_module(
        "promote_nimble_performance_baseline",
        PROMOTION_MODULE_PATH,
    )

    telemetry = {
        "gate": {
            "duration_seconds": 12.5,
        },
        "bundle": {
            "primary": {
                "bytes": 450000,
            },
            "secondary_chunk_count": 2,
            "chunks": [
                {
                    "kind": "primary",
                    "bytes": 450000,
                },
                {
                    "kind": "secondary",
                    "bytes": 50000,
                },
                {
                    "kind": "secondary",
                    "bytes": 25000,
                },
            ],
        },
    }

    metrics = module.build_metrics(
        telemetry
    )

    assert (
        metrics["primary_bundle_bytes"]
        == 450000
    )

    assert (
        metrics["total_javascript_bytes"]
        == 525000
    )

    assert (
        metrics[
            "largest_secondary_chunk_bytes"
        ]
        == 50000
    )


def test_current_baseline_has_required_contract():
    module = load_module(
        "validate_nimble_baseline_governance",
        VALIDATOR_MODULE_PATH,
    )

    baseline = json.loads(
        module.BASELINE.read_text(
            encoding="utf-8",
        )
    )

    assert (
        module.REQUIRED_METRICS
        <= set(baseline["metrics"])
    )

    assert (
        module.REQUIRED_THRESHOLDS
        <= set(baseline["thresholds"])
    )
