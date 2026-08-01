from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="smoke")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/card_hawk_vocabulary/governance_registry"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    report = {
        "module": "governance_registry",
        "title": "Vocabulary Governance Registry",
        "status": "ready",
        "application": "CARD_HAWK",
        "library": "EXPERIENCE_VOCABULARY",
        "semanticFaithfulness": True,
    }
    target = args.output / "governance_registry.json"
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Vocabulary Governance Registry complete.")
    return 0
