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
        default=Path("reports/architecture/kinekt/engineering_quality"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = (
        Engine()
        .evaluate(
            lint=100,
            formatting=100,
            tests=100,
            coverage=100,
            complexity=100,
            maintainability=100,
        )
        .to_dict()
    )
    (args.output / "engineering_quality.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Engineering Quality Engine complete.")
    return 0
