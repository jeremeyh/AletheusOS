from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .engine import EventPipeline


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("run",), nargs="?", default="run")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/event_pipeline"),
    )
    args = parser.parse_args()
    pipeline = EventPipeline(
        Path(
            "reports/architecture/kinekt/runtime_service_bus/runtime-service-bus.json"
        ),
        args.output,
    )
    report = asyncio.run(pipeline.run_default_flow())
    print(
        "Constitutional Event Pipeline complete: "
        f"events={report['event_count']}, channels={report['service_bus_channels']}."
    )
    return 0
