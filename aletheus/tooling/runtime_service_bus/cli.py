from __future__ import annotations

import argparse
from pathlib import Path

from .engine import ServiceBusEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/runtime_service_bus"),
    )
    args = parser.parse_args()
    report = ServiceBusEngine(
        Path("reports/architecture/kinekt/wiring/constitutional-wiring-manifest.json"),
        args.output,
    ).build()
    print(f"Runtime Service Bus complete: channels={report['channel_count']}.")
    return 0
