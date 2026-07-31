from __future__ import annotations

import importlib.util
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

VALIDATOR = ROOT / "validate_nimble_dependency_exceptions.py"

SCANNER = ROOT / "scan_nimble_dependency_risk.py"


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


def valid_exception():
    return {
        "id": "NIMBLE-DEP-EX-001",
        "ecosystem": "npm",
        "package": "example",
        "version": "1.0.0",
        "exception_type": "license_review",
        "subject": "unknown",
        "rationale": (
            "A reviewed temporary exception with sufficient documented justification."
        ),
        "approved_by": "Council",
        "owner": "Platform",
        "ticket": "SEC-1",
        "created_at": "2026-07-10T00:00:00+00:00",
        "expires_at": "2026-10-10T00:00:00+00:00",
        "status": "active",
    }


def test_valid_exception_contract():
    module = load_module(
        "dependency_exception_validator",
        VALIDATOR,
    )

    failures = module.validate_exception(
        valid_exception(),
        now=datetime(
            2026,
            7,
            11,
            tzinfo=UTC,
        ),
    )

    assert failures == []


def test_expired_active_exception_fails():
    module = load_module(
        "dependency_exception_validator",
        VALIDATOR,
    )

    item = valid_exception()
    item["expires_at"] = "2026-07-10T01:00:00+00:00"

    failures = module.validate_exception(
        item,
        now=datetime(
            2026,
            7,
            11,
            tzinfo=UTC,
        ),
    )

    assert "active exception has expired" in failures


def test_exception_matching_is_exact():
    module = load_module(
        "dependency_risk_scanner",
        SCANNER,
    )

    item = valid_exception()

    assert module.exception_matches(
        item,
        ecosystem="npm",
        package="example",
        version="1.0.0",
        exception_type="license_review",
        subject="unknown",
    )

    assert not module.exception_matches(
        item,
        ecosystem="npm",
        package="example",
        version="2.0.0",
        exception_type="license_review",
        subject="unknown",
    )
