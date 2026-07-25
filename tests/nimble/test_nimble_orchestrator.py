from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from nimble.orchestrator.discovery import (
    discover_capabilities,
)
from nimble.orchestrator.planner import (
    create_build_plan,
)

ROOT = Path(__file__).resolve().parents[2]

VALIDATOR = (
    ROOT
    / "tools"
    / "validation"
    / "nimble"
    / "validate_nimble_orchestrator.py"
)


def test_discovery_finds_known_capabilities() -> None:
    statuses = discover_capabilities(ROOT)

    identifiers = {
        status.capability_id
        for status in statuses
    }

    assert "experience-core" in identifiers
    assert "react-primitives" in identifiers
    assert "workspace-engine" in identifiers
    assert "founder-console" in identifiers


def test_founder_console_depends_on_primitives() -> None:
    statuses = {
        status.capability_id: status
        for status in discover_capabilities(ROOT)
    }

    founder = statuses["founder-console"]

    assert (
        "react-primitives"
        in founder.dependencies
    )

    assert founder.state in {
        "implemented",
        "partial",
        "planned",
        "blocked",
        "missing",
    }

    assert 0 <= founder.readiness_percent <= 100


def test_missing_dependencies_block_capabilities() -> None:
    statuses = discover_capabilities(ROOT)

    for status in statuses:
        if status.blocked_by:
            assert status.state == "blocked"

        if status.state == "blocked":
            assert status.blocked_by


def test_build_plan_is_dependency_aware() -> None:
    plan = create_build_plan(ROOT)

    capability_ids = [
        item.capability_id
        for item in plan
    ]

    assert len(capability_ids) == len(
        set(capability_ids)
    )

    assert all(
        item.state != "implemented"
        for item in plan
    )

    blocked_section_started = False

    for item in plan:
        if item.state == "blocked":
            blocked_section_started = True
            assert item.action == (
                "resolve dependencies"
            )
        else:
            assert not blocked_section_started


def test_cli_generates_report(
    tmp_path: Path,
) -> None:
    report_path = (
        tmp_path
        / "nimble-orchestrator-report.json"
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "nimble.orchestrator",
            "--root",
            str(ROOT),
            "--report",
            str(report_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=240,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )

    assert report_path.is_file()

    report = json.loads(
        report_path.read_text(
            encoding="utf-8"
        )
    )

    assert report["schema_version"] == "1.0"
    assert "capabilities" in report
    assert isinstance(
        report["capabilities"],
        list,
    )

    capability_ids = {
        capability["capability_id"]
        for capability in report[
            "capabilities"
        ]
    }

    assert "experience-core" in capability_ids
    assert "react-primitives" in capability_ids
    assert "workspace-engine" in capability_ids
    assert "founder-console" in capability_ids


def test_orchestrator_validator_passes() -> None:
    assert VALIDATOR.is_file(), (
        f"Validator not found: {VALIDATOR}"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=240,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )
