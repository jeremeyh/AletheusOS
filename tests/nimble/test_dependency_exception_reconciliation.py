from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "reconcile_nimble_dependency_exceptions.py"


def load_module():
    specification = importlib.util.spec_from_file_location(
        "dependency_exception_reconciliation",
        MODULE_PATH,
    )

    assert specification is not None
    assert specification.loader is not None

    module = importlib.util.module_from_spec(specification)

    specification.loader.exec_module(module)

    return module


def exception():
    return {
        "id": "NIMBLE-DEP-EX-001",
        "ecosystem": "npm",
        "package": "example",
        "version": "1.0.0",
        "exception_type": "license_review",
        "subject": "unknown",
        "status": "active",
    }


def risk_report():
    return {
        "licenses": {
            "allowed": [],
            "review_required": [
                {
                    "ecosystem": "npm",
                    "name": "example",
                    "version": "1.0.0",
                    "license": "unknown",
                }
            ],
            "denied": [],
        },
        "npm_audit": {
            "available": True,
            "vulnerabilities": [],
        },
        "python_audit": {
            "available": True,
            "dependencies": [],
        },
    }


def test_exact_exception_matches_current_risk():
    module = load_module()

    result = module.reconcile(
        {
            "exceptions": [
                exception(),
            ]
        },
        risk_report(),
    )

    assert len(result["matched"]) == 1
    assert result["orphaned"] == []
    assert result["failures"] == []


def test_orphaned_exception_fails():
    module = load_module()

    report = risk_report()
    report["licenses"]["review_required"] = []

    result = module.reconcile(
        {
            "exceptions": [
                exception(),
            ]
        },
        report,
    )

    assert len(result["orphaned"]) == 1
    assert result["failures"]


def test_duplicate_active_exception_fails():
    module = load_module()

    second = {
        **exception(),
        "id": "NIMBLE-DEP-EX-002",
    }

    result = module.reconcile(
        {
            "exceptions": [
                exception(),
                second,
            ]
        },
        risk_report(),
    )

    assert len(result["duplicate_exceptions"]) == 2
    assert result["failures"]


def test_unwaived_denied_license_fails():
    module = load_module()

    report = risk_report()
    report["licenses"]["review_required"] = []
    report["licenses"]["denied"] = [
        {
            "ecosystem": "npm",
            "name": "restricted",
            "version": "2.0.0",
            "license": "AGPL-3.0",
        }
    ]

    result = module.reconcile(
        {"exceptions": []},
        report,
    )

    assert len(result["unwaived_enforceable_risks"]) == 1
    assert result["failures"]
