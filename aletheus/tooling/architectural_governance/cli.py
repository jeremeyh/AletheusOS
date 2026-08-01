from __future__ import annotations

import argparse
from pathlib import Path

from .engine import GovernanceEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("evaluate", "validate"),
        nargs="?",
        default="evaluate",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/governance"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = GovernanceEngine(
        root / "authority/capability-authority-map.json",
        root / "boundary/runtime-boundaries.json",
        root / "health/constitutional-health.json",
        root / "registry/constitutional-registry.json",
        args.output,
    ).evaluate()
    print(
        "Architectural Governance complete: "
        f"decision={report['decision']}, "
        f"critical={report['critical']}, "
        f"high={report['high']}."
    )
    if args.command == "validate" and report["decision"] == "block":
        return 1
    return 0
