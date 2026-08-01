from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("verify",),
        nargs="?",
        default="verify",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/post_install_health"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "process_composer/constitutional-process-composition.json",
        root / "runtime_service_bus/runtime-service-bus.json",
        args.output,
    ).verify()
    print(f"Post-install Health complete: healthy={report['healthy']}.")
    return 0 if report["healthy"] else 1
