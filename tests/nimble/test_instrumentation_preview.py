from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

INSTRUMENTATION = (
    ROOT
    / "nimble/packages/react/src/instrumentation"
)

SHOWCASE = (
    ROOT
    / "nimble/apps/platform-shell/src/nimble/"
    "showcase/IntelligenceInstrumentationShowcase.tsx"
)

CSS = SHOWCASE.with_name(
    "instrumentation-preview.css"
)


def read(
    relative: str,
) -> str:
    return (
        INSTRUMENTATION / relative
    ).read_text(
        encoding="utf-8"
    )


def test_instrumentation_is_exported() -> None:
    index = (
        ROOT
        / "nimble/packages/react/src/index.ts"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        'export * from "./instrumentation";'
        in index
    )


def test_reserved_instrument_names_are_canonical() -> None:
    canonical = read(
        "canonical.ts"
    )

    assert (
        '"Aletheus Index™"'
        in canonical
    )

    assert (
        '"THORᵡ"'
        in canonical
    )


def test_engine_identities_are_canonical() -> None:
    canonical = read(
        "canonical.ts"
    )

    for engine in [
        "Evidence Engine™",
        "Knowledge Engine™",
        "Reason Engine™",
        "Memory Engine™",
        "Bias Engine™",
        "Risk Engine™",
        "Predictive Engine™",
    ]:
        assert engine in canonical


def test_registry_rejects_duplicates() -> None:
    registry = read(
        "registry.ts"
    )

    assert (
        "Duplicate instrument"
        in registry
    )


def test_reserved_identity_is_protected() -> None:
    validation = read(
        "validation.ts"
    )

    assert (
        "Reserved instrument cannot be renamed"
        in validation
    )


def test_formatting_is_deterministic() -> None:
    formatting = read(
        "formatting.ts"
    )

    assert (
        'return value.toFixed(1);'
        in formatting
    )

    assert (
        'toFixed(1)}%`'
        in formatting
    )


def test_showcase_separates_top_level_instruments() -> None:
    text = SHOWCASE.read_text(
        encoding="utf-8"
    )

    assert (
        "AletheusIndexInstrument"
        in text
    )

    assert (
        "ThorxInstrument"
        in text
    )

    assert (
        "Council Consensus"
        not in text
    )


def test_showcase_contains_engine_grid() -> None:
    text = SHOWCASE.read_text(
        encoding="utf-8"
    )

    assert (
        "ENGINE_INSTRUMENT_IDS"
        in text
    )

    assert (
        "Individual Engine Grades"
        in text
    )


def test_preview_is_responsive_and_accessible() -> None:
    css = CSS.read_text(
        encoding="utf-8"
    )

    assert (
        "@media (max-width: 900px)"
        in css
    )

    assert (
        "prefers-reduced-motion"
        in css
    )


def test_instrumentation_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_instrumentation_preview.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=360,
    )

    assert result.returncode == 0, (
        result.stdout
        + result.stderr
    )

    assert (
        "Status: PASS"
        in result.stdout
    )
