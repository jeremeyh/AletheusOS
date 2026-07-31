#!/usr/bin/env python3
"""
Backward-compatible entry point.

Canonical implementation:
    tools/collect/collect_nimble_production_telemetry.py
"""

from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TARGET = ROOT / "tools" / "collect" / "collect_nimble_production_telemetry.py"

if not TARGET.exists():
    raise FileNotFoundError(f"Canonical telemetry collector not found:\n{TARGET}")

if __name__ == "__main__":
    runpy.run_path(
        str(TARGET),
        run_name="__main__",
    )
else:
    globals().update(runpy.run_path(str(TARGET)))
