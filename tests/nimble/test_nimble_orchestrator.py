from __future__ import annotations

import json
import subprocess
from pathlib import Path

from nimble.orchestrator.discovery import (
    discover_capabilities,
)
from nimble.orchestrator.planner import (
    create_build_plan,
)


ROOT = Path(__file__).resolve().parents[2]


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
        for status in discover_capabilities(
            ROOT
        )
    }

    founder = statuses["founder-console"]

    assert "react-primitives" in (
        founder.dependencies
    )

    assert "workspace-engine" in (
        founder.dependencies
    )


def test_missing_dependencies_block_capabilities() -> None:
    statuses = {
        status.capability_id: status
        for status in discover_capabilities(
            ROOT
        )
    }

    primitives = statuses[
        "react-primitives"
    ]

    founder = statuses[
        "founder-console"
    ]

    if primitives.state != "implemented":
        assert (
            founder.state == "blocked"
            or founder.state == "implemented"
        )


def test_build_plan_is_dependency_aware() -> None:
    plan = create_build_plan(ROOT)

    identifiers = [
        item.capability_id
        for item in plan
    ]

    if (
        "react-primitives"
        in identifiers
        and "founder-console"
        in identifiers
    ):
        assert (
            identifiers.index(
                "react-primitives"
            )
            < identifiers.index(
                "founder-console"
            )
        )


def test_cli_generates_report() -> None:
    result = subprocess.run(
        [
            "python",
            "-m",
            "nimble.orchestrator",
            "--root",
            str(ROOT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )

    report_path = (
        ROOT
        / "reports/nimble/orchestrator/"
        "build-state-latest.json"
    )

    assert report_path.is_file()

    report = json.loads(
        report_path.read_text(
            encoding="utf-8"
        )
    )

    assert (
        report["schema_version"]
        == "1.0"
    )

    assert "build_plan" in report


def test_orchestrator_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_orchestrator.py"
            ),
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

    assert "Status: PASS" in result.stdout
