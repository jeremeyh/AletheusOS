#!/usr/bin/env python3
"""
Backward-compatible entry point.

Canonical implementation:
    tools/nimble/generate_release_attestation.py
"""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

TARGET = ROOT / "tools" / "nimble" / "generate_release_attestation.py"


def _require_target() -> Path:
    if not TARGET.is_file():
        raise FileNotFoundError(f"Canonical generator not found:\n{TARGET}")
    return TARGET


def _export_namespace() -> dict[str, Any]:
    namespace = runpy.run_path(str(_require_target()))

    for name, value in namespace.items():
        if not name.startswith("__"):
            globals().setdefault(name, value)

    return namespace


if __name__ == "__main__":
    runpy.run_path(
        str(_require_target()),
        run_name="__main__",
    )
else:
    _export_namespace()
