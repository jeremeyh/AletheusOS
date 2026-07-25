from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PRIMITIVES = (
    ROOT
    / "nimble/packages/react/src/primitives"
)


def read(
    relative: str,
) -> str:
    return (
        PRIMITIVES / relative
    ).read_text(
        encoding="utf-8"
    )


def test_react_package_exports_primitives() -> None:
    index = (
        ROOT
        / "nimble/packages/react/src/index.ts"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        'export * from "./primitives";'
        in index
    )


def test_surface_is_token_driven() -> None:
    surface = read(
        "Surface.tsx"
    )

    assert "surface.canvas" in surface
    assert "elevation.hud" in surface
    assert "radius.lg" in surface


def test_stack_is_token_driven() -> None:
    stack = read(
        "Stack.tsx"
    )

    assert "space.0" in stack
    assert "space.16" in stack


def test_grid_supports_adaptive_layout() -> None:
    grid = read(
        "Grid.tsx"
    )

    assert "auto-fit" in grid
    assert "minmax" in grid


def test_text_supports_instrument_roles() -> None:
    text = read(
        "Text.tsx"
    )

    assert '"instrument"' in text
    assert '"telemetry"' in text
    assert (
        "font.family.instrument"
        in text
    )


def test_visualization_primitives_exist() -> None:
    assert (
        "data-nimble-primitive=\"meter\""
        in read("Meter.tsx")
    )

    assert (
        "data-nimble-primitive=\"signal\""
        in read("Signal.tsx")
    )


def test_instrument_supports_density_profiles() -> None:
    instrument = read(
        "Instrument.tsx"
    )

    for density in [
        "consumer",
        "enterprise",
        "founder",
    ]:
        assert density in instrument


def test_reserved_instrument_identity_is_immutable() -> None:
    reserved = read(
        "reserved.tsx"
    )

    assert (
        'id="instrument.aletheus-index"'
        in reserved
    )

    assert (
        'label="Aletheus Index™"'
        in reserved
    )

    assert (
        'id="instrument.thorx"'
        in reserved
    )

    assert (
        'label="THORᵡ"'
        in reserved
    )


def test_primitive_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_primitive_experience.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=240,
    )

    assert result.returncode == 0, (
        result.stdout
        + result.stderr
    )

    assert (
        "Status: PASS"
        in result.stdout
    )
