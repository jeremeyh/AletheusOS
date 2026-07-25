#!/usr/bin/env python3
"""
Backward-compatible entry point.

Canonical implementation:
    tools/promotion/promote_nimble_performance_baseline.py
"""

from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent

TARGET = (
    ROOT
    / "tools"
    / "promotion"
    / "promote_nimble_performance_baseline.py"
)

if not TARGET.exists():
    raise FileNotFoundError(
        f"Canonical promotion tool not found:\n{TARGET}"
    )


def _load():
    namespace = runpy.run_path(str(TARGET))
    globals().update(namespace)
    return namespace


if __name__ == "__main__":
    runpy.run_path(
        str(TARGET),
        run_name="__main__",
    )
else:
    _load()
