from __future__ import annotations

import argparse
from pathlib import Path

from .engine import RegistryEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/registry"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = RegistryEngine(
        root / "authority/capability-authority-map.json",
        root / "twin/architectural-digital-twin.json",
        args.output,
    ).build()
    print(
        "Constitutional Registry complete: "
        f"capabilities={len(report['capabilities'])}, "
        f"entities={len(report['entities'])}."
    )
    return 0
