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
        default=Path("reports/architecture/kinekt/spartan_runtime"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "ecosystem_catalog/canonical-ecosystem-catalog.json",
        root / "runtime_service_bus/runtime-service-bus.json",
        args.output,
    ).build()
    print(
        "SPARTAN Runtime Integration complete: "
        f"components={len(report['components'])}, mode={report['integration_mode']}."
    )
    return 0
