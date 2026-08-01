from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine, Migration


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("run",), nargs="?", default="run")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/schema_evolution"),
    )
    args = parser.parse_args()
    engine = Engine(args.output)
    engine.register(
        Migration(
            "bootstrap-v1",
            0,
            1,
            lambda payload: {**payload, "migrated": True},
        )
    )
    result = engine.migrate({"schema_version": 0}, 1)
    engine.write_report(result)
    print("Schema Evolution complete: version=1.")
    return 0
