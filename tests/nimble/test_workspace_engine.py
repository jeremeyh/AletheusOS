from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ENGINE_ROOT = (
    ROOT
    / "nimble/packages/workspace/src/engine"
)


def read(relative: str) -> str:
    return (
        ENGINE_ROOT / relative
    ).read_text(encoding="utf-8")


def test_workspace_package_exports_engine() -> None:
    index = (
        ROOT
        / "nimble/packages/workspace/src/index.ts"
    ).read_text(encoding="utf-8")

    assert (
        'export * from "./engine";'
        in index
    )


def test_workspace_registry_exists() -> None:
    assert "class WorkspaceRegistry" in read(
        "registry.ts"
    )


def test_workspace_regions_are_canonical() -> None:
    contracts = read("contracts.ts")

    for region in [
        "navigation",
        "canvas",
        "activity-rail",
        "status-bar",
        "inspector",
        "overlay",
    ]:
        assert f'"{region}"' in contracts


def test_panel_dock_states_are_governed() -> None:
    contracts = read("contracts.ts")

    for state in [
        "left",
        "right",
        "bottom",
        "floating",
        "detached",
        "hidden",
    ]:
        assert f'"{state}"' in contracts


def test_layout_validation_exists() -> None:
    layout = read("layout.ts")

    assert "validateWorkspaceLayout" in layout
    assert "duplicate panel" in layout
    assert "unknown panel" in layout


def test_workspace_persistence_is_versioned() -> None:
    persistence = read("persistence.ts")

    assert 'schemaVersion: "1.0"' in persistence
    assert "Invalid workspace snapshot" in persistence


def test_founder_console_is_reference_workspace() -> None:
    founder = read("founder.ts")

    assert "Founder Console™" in founder
    assert "Intelligence Instrumentation™" in founder
    assert '"founder"' in founder


def test_workspace_engine_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_workspace_engine.py"
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
