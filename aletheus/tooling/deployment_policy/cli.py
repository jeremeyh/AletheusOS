from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("evaluate",),
        nargs="?",
        default="evaluate",
    )
    parser.add_argument("--environment", default="production")
    parser.add_argument("--certification", default="READY")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/deployment_policy"),
    )
    args = parser.parse_args()
    report = Engine(args.output).evaluate(
        args.environment,
        args.certification,
    )
    print(f"Deployment Policy complete: allowed={report['allowed']}.")
    return 0 if report["allowed"] else 1
