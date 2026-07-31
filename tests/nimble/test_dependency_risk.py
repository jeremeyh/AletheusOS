from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scan_nimble_dependency_risk.py"


def load_module():
    specification = importlib.util.spec_from_file_location(
        "scan_nimble_dependency_risk",
        MODULE_PATH,
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(specification)

    specification.loader.exec_module(module)

    return module


def test_license_normalization():
    module = load_module()

    assert module.normalize_license(None) == "unknown"
    assert module.normalize_license("") == "unknown"
    assert module.normalize_license("MIT") == "MIT"


def test_denied_license_classification():
    module = load_module()

    manifest = {
        "npm": {
            "resolved_packages": [
                {
                    "name": "example",
                    "version": "1.0.0",
                    "license": "AGPL-3.0",
                }
            ]
        },
        "python": {
            "installed_packages": [],
        },
    }

    policy = {
        "licenses": {
            "allowed": ["MIT"],
            "review_required": ["unknown"],
            "denied": ["AGPL-3.0"],
        }
    }

    result = module.classify_licenses(
        manifest,
        policy,
    )

    assert len(result["denied"]) == 1
    assert result["denied"][0]["name"] == "example"


def test_npm_vulnerability_threshold():
    module = load_module()

    audit = {
        "available": True,
        "counts": {
            "critical": 1,
            "high": 0,
        },
    }

    policy = {
        "vulnerabilities": {
            "maximum_accepted": {
                "critical": 0,
                "high": 0,
            }
        }
    }

    failures = module.evaluate_npm_vulnerabilities(
        audit,
        policy,
    )

    assert failures
