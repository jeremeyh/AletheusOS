from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("run",), nargs="?", default="run")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/transaction_coordinator"),
    )
    args = parser.parse_args()
    engine = Engine(args.output)
    transaction = engine.begin("genesis-20.1-smoke", ["19.7", "19.8"])
    engine.checkpoint(transaction, "19.7", "pending")
    report = engine.commit(transaction)
    print(f"Transaction Coordinator complete: status={report['status']}.")
    return 0
