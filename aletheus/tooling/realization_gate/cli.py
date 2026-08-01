from __future__ import annotations

import argparse
from pathlib import Path

from .engine import RealizationGateEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=("evaluate", "validate"), nargs="?", default="evaluate"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/realization_gate"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = RealizationGateEngine(
        root / "authority_ledger/constitutional-authority-ledger.json",
        root / "ecosystem_catalog/canonical-ecosystem-catalog.json",
        root / "mesh_synthesis/mesh-synthesis-graph.json",
        root / "governance/governance-findings.json",
        args.output,
    ).evaluate()
    print(
        "Ecosystem Realization Gate complete: "
        f"decision={report['decision']}, "
        f"realized={report['ledger_realized']}/{report['ledger_entries']}, "
        f"catalog={report['catalog_entries']}."
    )
    if args.command == "validate" and report["decision"] == "block":
        return 1
    return 0
