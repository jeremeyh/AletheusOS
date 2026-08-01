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
        default=Path("reports/architecture/kinekt/claim_envelopes"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "ecosystem_catalog/canonical-ecosystem-catalog.json",
        root / "root_domain_resolution/explicit-root-domain-resolution.json",
        args.output,
    ).build()
    print(f"Claim Envelope complete: ambivalent={report['ambivalent_claim_count']}.")
    return 0
