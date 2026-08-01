import argparse
from pathlib import Path

from .engine import AuthorityLedgerEngine


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("build", "validate"), nargs="?", default="build")
    p.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/authority_ledger"),
    )
    a = p.parse_args()
    root = Path("reports/architecture/kinekt")
    r = AuthorityLedgerEngine(
        Path("config/authority_ledger/canonical_authority_catalog.json"),
        root / "authority/capability-authority-map.json",
        root / "registry/constitutional-registry.json",
        root / "twin/architectural-digital-twin.json",
        root / "knowledge_graph/runtime-knowledge-graph.json",
        root / "governance/governance-findings.json",
        Path("."),
        a.output,
    ).build()
    critical = sum(f.get("severity") == "critical" for f in r["findings"])
    print(
        f"Constitutional Authority Ledger complete: entries={len(r['entries'])}, realized={r['maturity_counts']['realized']}, findings={len(r['findings'])}, critical={critical}."
    )
    return 1 if a.command == "validate" and critical else 0
