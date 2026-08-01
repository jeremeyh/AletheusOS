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
        default=Path("reports/architecture/kinekt/runtime_reliability"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = (
        Engine()
        .evaluate(
            lifecycle=100,
            scheduler=100,
            event_latency=100,
            resilience=100,
            saturation=100,
            async_correctness=100,
        )
        .to_dict()
    )
    (args.output / "runtime_reliability.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Runtime Reliability Engine complete.")
    return 0
