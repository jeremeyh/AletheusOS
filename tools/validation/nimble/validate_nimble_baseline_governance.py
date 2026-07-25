#!/usr/bin/env python3
"""
Nimble Baseline Governance Validator

Validates the repository performance baseline contract.

This implementation discovers the repository root dynamically by
searching upward for pyproject.toml so it continues to work regardless
of where the validator resides.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    """
    Locate the repository root by searching upward for pyproject.toml.
    """
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError(
                "Unable to locate repository root (pyproject.toml)."
            )

        current = current.parent


REPO_ROOT = find_repo_root(Path(__file__).parent)



REQUIRED_METRICS = {
    "gate_duration_seconds",
    "largest_secondary_chunk_bytes",
    "primary_bundle_bytes",
    "secondary_chunk_count",
    "total_javascript_bytes",
}



REQUIRED_THRESHOLDS = {
    "gate_duration_absolute_limit_seconds",
    "gate_duration_growth_percent",
    "largest_secondary_growth_percent",
    "primary_bundle_absolute_limit_bytes",
    "primary_bundle_growth_percent",
    "secondary_chunk_count_decrease_allowed",
    "secondary_chunk_count_increase_allowed",
    "total_javascript_growth_percent",
}

BASELINE = (
    REPO_ROOT
    / "nimble"
    / "governance"
    / "performance-baseline.json"
)


def load_baseline() -> dict:
    if not BASELINE.exists():
        raise FileNotFoundError(
            f"Performance baseline not found: {BASELINE}"
        )

    return json.loads(
        BASELINE.read_text(encoding="utf-8")
    )


def validate() -> bool:
    baseline = load_baseline()

    required = (
        "metrics",
        "generated_at",
    )

    missing = [
        key
        for key in required
        if key not in baseline
    ]

    if missing:
        raise ValueError(
            "Missing required baseline keys: "
            + ", ".join(missing)
        )

    return True


def main() -> int:
    try:
        validate()
        print("✓ Baseline governance validation passed.")
        return 0

    except Exception as exc:
        print(f"✗ {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
