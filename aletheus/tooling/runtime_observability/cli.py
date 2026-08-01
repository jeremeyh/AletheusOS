from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/runtime_observability"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "runtime_telemetry/runtime-telemetry.json",
        root / "observatory/platform-observatory.json",
        args.output,
    ).build()
    print(
        "Runtime Observability complete: "
        f"records={report['telemetry_records']}, readiness={report['readiness']}."
    )
    return 0
