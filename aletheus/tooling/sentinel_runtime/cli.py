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
        default=Path("reports/architecture/kinekt/sentinel_runtime"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "spartan_runtime/spartan-runtime-integration.json",
        root / "runtime_observability/runtime-observability.json",
        root / "runtime_diagnostics/constitutional-runtime-diagnostics.json",
        root / "governance/governance-findings.json",
        args.output,
    ).build()
    print(
        "Sentinel Platform Runtime complete: "
        f"readiness={report['readiness']}, response={report['response_mode']}."
    )
    return 0
