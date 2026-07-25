#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError(
                "Unable to locate repository root."
            )

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger-contract.json"
)

LEDGER_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger.jsonl"
)

FORBIDDEN_KEY_PATTERN = re.compile(
    r"(secret|password|token|credential)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# KEEP THE REMAINDER OF YOUR EXISTING FILE UNCHANGED BELOW THIS POINT.
# Replace only the header/root-resolution section.
# ---------------------------------------------------------------------------
