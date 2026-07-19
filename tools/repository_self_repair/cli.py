#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from aletheus.repository_self_repair import RepositorySelfRepairEngine


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AletheusOS Repository Self-Repair and Convergence Engine")
    p.add_argument("target", type=Path, help="Canonical Git-backed repository")
    p.add_argument("--source", type=Path, help="Secondary repository/snapshot to merge")
    p.add_argument("--apply", action="store_true", help="Apply the generated plan; default is dry-run")
    p.add_argument("--delete-known-orphans", action="store_true", help="Permanently delete policy-confirmed debris instead of quarantining it")
    p.add_argument("--archive-source", action="store_true", help="Create a checksummed tar.gz of the source after successful execution")
    p.add_argument("--remove-source", action="store_true", help="Remove source only after a successful archive; requires --archive-source and --apply")
    p.add_argument("--archive-root", type=Path)
    p.add_argument("--report-root", type=Path)
    p.add_argument("--monitor", action="store_true", help="Run continuous non-destructive self-repair")
    p.add_argument("--interval", type=int, default=3600, help="Monitor interval in seconds (minimum 60)")
    return p


def main() -> int:
    args = parser().parse_args()
    if args.remove_source and not args.archive_source:
        raise SystemExit("--remove-source requires --archive-source")
    if args.remove_source and not args.apply:
        raise SystemExit("--remove-source requires --apply")
    engine = RepositorySelfRepairEngine()
    if args.monitor:
        if args.source:
            raise SystemExit("continuous monitor does not merge a source; run explicit convergence first")
        engine.monitor(args.target, interval_seconds=args.interval, report_root=args.report_root)
        return 0
    plan, result, report = engine.run(
        args.target,
        args.source,
        apply=args.apply,
        delete_known_orphans=args.delete_known_orphans,
        archive_source=args.archive_source,
        remove_source=args.remove_source,
        archive_root=args.archive_root,
        report_root=args.report_root,
    )
    print(json.dumps({"counts": plan.counts(), "success": result.success, "dry_run": result.dry_run, "archive": result.archive_path, "report": str(report)}, indent=2))
    return 0 if result.success else 2


if __name__ == "__main__":
    raise SystemExit(main())
