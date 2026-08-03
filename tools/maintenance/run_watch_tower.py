import argparse
import json
from pathlib import Path

from watch_tower.runtime.engine import WatchTowerEngine


def main():
    parser = argparse.ArgumentParser(description="Watch Tower™ integrity scanner")
    parser.add_argument("--repair", action="store_true", help="Apply safe repairs")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    root = Path.cwd()
    engine = WatchTowerEngine(root)

    if args.repair:
        result = engine.repair()
    else:
        result = engine.scan()

    reports = engine.write_reports()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        wt = result["watch_tower"]
        print()
        print("=" * 72)
        print("Watch Tower™")
        print("=" * 72)
        print(f"Status : {wt['status']}")
        print(f"Score  : {wt['score']}")
        print(f"Root   : {wt['root']}")
        print()
        print("Findings:")
        for severity, count in wt["counts"].items():
            print(f"  {severity:<8} {count}")
        print()
        print(f"Markdown report: {reports['markdown']}")
        print(f"JSON report    : {reports['json']}")
        print("=" * 72)


if __name__ == "__main__":
    main()
