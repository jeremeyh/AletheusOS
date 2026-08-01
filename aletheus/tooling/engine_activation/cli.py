from __future__ import annotations

import argparse
from pathlib import Path

from .engine import ActivationManager


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("activate",), nargs="?", default="activate")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/engine_activation"),
    )
    args = parser.parse_args()
    manager = ActivationManager(
        Path(
            "reports/architecture/kinekt/engine_registry_realization/engine-registry-realization.json"
        ),
        args.output,
    )
    report = manager.activate_all()
    print(
        "Engine Activation complete: "
        f"active={report['activated_count']}, failed={report['failed_count']}."
    )
    return 0 if report["failed_count"] == 0 else 1
