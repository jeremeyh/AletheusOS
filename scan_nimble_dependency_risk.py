#!/usr/bin/env python3
"""
Backward-compatible entry point.

Canonical implementation:
    tools/scanning/scan_nimble_dependency_risk.py
"""

from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TARGET = (
    ROOT
    / "tools"
    / "scanning"
    / "scan_nimble_dependency_risk.py"
)

if not TARGET.exists():
    raise FileNotFoundError(
        f"Canonical dependency risk scanner not found:\n{TARGET}"
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
