from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "validate_nimble_performance_regression.py"


def load_module():
    specification = importlib.util.spec_from_file_location(
        "validate_nimble_performance_regression",
        MODULE_PATH,
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)

    return module


def test_percent_change():
    module = load_module()

    assert (
        module.percent_change(
            105,
            100,
        )
        == 5.0
    )


def test_metric_passes_within_threshold():
    module = load_module()

    result = module.metric_result(
        name="Example",
        current=104,
        baseline=100,
        allowed_growth_percent=5,
        absolute_limit=110,
    )

    assert result["status"] == "PASS"
    assert result["failures"] == []


def test_metric_fails_growth_threshold():
    module = load_module()

    result = module.metric_result(
        name="Example",
        current=106,
        baseline=100,
        allowed_growth_percent=5,
    )

    assert result["status"] == "FAIL"
    assert result["failures"]


def test_metric_fails_absolute_limit():
    module = load_module()

    result = module.metric_result(
        name="Example",
        current=501000,
        baseline=450000,
        absolute_limit=500000,
    )

    assert result["status"] == "FAIL"
