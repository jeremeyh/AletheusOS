from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("certify",),
        nargs="?",
        default="certify",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/production_readiness"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "post_install_health/post-install-health.json",
        root / "runtime_compatibility/runtime-compatibility-matrix.json",
        args.output,
    ).certify()
    print(f"Production Readiness complete: status={report['status']}.")
    return 0 if report["status"] == "READY" else 1
