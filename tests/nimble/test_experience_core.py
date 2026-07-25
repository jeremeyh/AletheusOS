from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXPERIENCE_ROOT = (
    ROOT
    / "nimble/packages/core/src/experience"
)


def read(relative: str) -> str:
    return (
        EXPERIENCE_ROOT / relative
    ).read_text(encoding="utf-8")


def test_experience_core_is_exported() -> None:
    index = (
        ROOT
        / "nimble/packages/core/src/index.ts"
    ).read_text(encoding="utf-8")

    assert 'export * from "./experience";' in index


def test_token_registry_exists() -> None:
    assert "class TokenRegistry" in read(
        "tokens/registry.ts"
    )


def test_theme_registry_exists() -> None:
    assert "class ThemeRegistry" in read(
        "theme/registry.ts"
    )


def test_aletheus_index_is_independent_instrument() -> None:
    contracts = read("contracts.ts")

    assert '"aletheus-index"' in contracts
    assert '"thorx"' in contracts


def test_canonical_engines_are_instrumented() -> None:
    instrumentation = read(
        "tokens/instrumentation.ts"
    )

    for engine in [
        "evidence",
        "knowledge",
        "reason",
        "memory",
        "bias",
        "risk",
        "predictive",
    ]:
        assert (
            f"instrumentation.engine.{engine}"
            in instrumentation
        )


def test_thorx_has_reserved_identity() -> None:
    instrumentation = read(
        "tokens/instrumentation.ts"
    )

    assert (
        "instrumentation.thorx.authorized"
        in instrumentation
    )

    assert (
        "instrumentation.thorx.rejected"
        in instrumentation
    )


def test_instrumentation_theme_exists() -> None:
    themes = read("theme/themes.ts")

    assert (
        'id: "aletheus.instrumentation"'
        in themes
    )


def test_experience_core_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_experience_core.py"
            ),
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

    assert "Status: PASS" in result.stdout
