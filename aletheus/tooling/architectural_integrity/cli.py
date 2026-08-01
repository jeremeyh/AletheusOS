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
        default=Path("reports/architecture/kinekt/architectural_integrity"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = (
        Engine()
        .evaluate(
            boundaries=100,
            cycles=100,
            registry=100,
            authority=100,
            cohesion=100,
            constitutional_compliance=100,
        )
        .to_dict()
    )
    (args.output / "architectural_integrity.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Architectural Integrity Engine complete.")
    return 0
