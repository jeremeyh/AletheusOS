#!/usr/bin/env python3
"""
Backward-compatible entry point.

Canonical implementation:
    tools/reconciliation/reconcile_nimble_dependency_exceptions.py
"""

from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TARGET = (
    ROOT
    / "tools"
    / "reconciliation"
    / "reconcile_nimble_dependency_exceptions.py"
)

if not TARGET.exists():
    raise FileNotFoundError(
        f"Canonical dependency reconciliation tool not found:\n{TARGET}"
    )

if __name__ == "__main__":
    runpy.run_path(
        str(TARGET),
        run_name="__main__",
    )
else:
    globals().update(
        runpy.run_path(str(TARGET))
    )
