from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="smoke")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/operational_excellence"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = (
        Engine()
        .evaluate(
            deployability=100,
            rollback=100,
            backup=100,
            provenance=100,
            compatibility=100,
            recovery=100,
        )
        .to_dict()
    )
    (args.output / "operational_excellence.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Operational Excellence Engine complete.")
    return 0
