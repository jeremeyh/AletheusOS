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
        default=Path("reports/architecture/kinekt/root_domain_resolution"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "semantic_topology/semantic-root-classification.json",
        root / "ecosystem_catalog/canonical-ecosystem-catalog.json",
        args.output,
    ).build()
    print(
        f"Root Domain Resolution complete: resolved={report['resolved_count']}, unresolved={len(report['unresolved_roots'])}."
    )
    return 0
