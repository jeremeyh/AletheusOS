from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=("build", "validate"), nargs="?", default="build"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/platform_continuity"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "vertical_slice_verification/vertical-slice-verification.json",
        root / "horizontal_mesh_verification/horizontal-mesh-verification.json",
        root / "access_modules/access-module-realization.json",
        root / "governance/governance-findings.json",
        args.output,
    ).build()
    print(f"Full Platform Continuity Gate complete: decision={report['decision']}.")
    if args.command == "validate" and report["decision"] == "block":
        return 1
    return 0
