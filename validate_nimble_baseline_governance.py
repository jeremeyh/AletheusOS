#!/usr/bin/env python3
"""Backward-compatible entry point for Nimble baseline governance validation.

Canonical implementation:
    tools/validation/nimble/validate_nimble_baseline_governance.py
"""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
TARGET = (
    ROOT / "tools" / "validation" / "nimble" / "validate_nimble_baseline_governance.py"
)


def _require_target() -> Path:
    if not TARGET.is_file():
        raise FileNotFoundError(
            f"Canonical Nimble baseline-governance validator was not found: {TARGET}"
        )

    return TARGET


def _export_canonical_namespace() -> dict[str, Any]:
    """Load the canonical module and expose its public API."""

    namespace = runpy.run_path(str(_require_target()))

    for name, value in namespace.items():
        if name.startswith("__"):
            continue

        globals().setdefault(name, value)

    return namespace


if __name__ == "__main__":
    runpy.run_path(
        str(_require_target()),
        run_name="__main__",
    )
else:
    _export_canonical_namespace()
