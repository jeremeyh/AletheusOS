#!/usr/bin/env python3
"""
Compatibility launcher.

This file exists because legacy compatibility tests invoke:

    python validate_nimble_audit_recovery_contract.py
"""

from __future__ import annotations

from pathlib import Path
from runpy import run_path


def _find_repo_root() -> Path:
    current = Path(__file__).resolve().parent

    while True:
        if (current / "tools").is_dir() and (current / "nimble").is_dir():
            return current

        if current.parent == current:
            raise RuntimeError(
                "Unable to locate repository root."
            )

        current = current.parent


ROOT = _find_repo_root()


def main() -> int:
    run_path(
        str(
            ROOT
            / "tools"
            / "validation"
            / "nimble"
            / "validate_nimble_audit_recovery_contract.py"
        ),
        run_name="__main__",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
