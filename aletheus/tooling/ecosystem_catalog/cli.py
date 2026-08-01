from __future__ import annotations

import argparse
from pathlib import Path

from .engine import EcosystemCatalogEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/ecosystem_catalog"),
    )
    args = parser.parse_args()
    report = EcosystemCatalogEngine(
        Path("config/authority_ledger/canonical_authority_catalog.json"),
        Path("config/authority_ledger/ecosystem_catalog_expansion.json"),
        args.output,
    ).build()
    print(f"Ecosystem Catalog complete: entries={len(report['entries'])}.")
    return 0
