from __future__ import annotations

import argparse
from pathlib import Path

from .engine import DataContractEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/data_contracts"),
    )
    args = parser.parse_args()
    report = DataContractEngine(
        Path(
            "reports/architecture/kinekt/runtime_service_bus/runtime-service-bus.json"
        ),
        args.output,
    ).build()
    print(
        f"Constitutional Data Contracts complete: contracts={report['contract_count']}."
    )
    return 0
