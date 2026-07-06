import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aletheus.boot import LighthouseBootloader


def main():
    parser = argparse.ArgumentParser(description="Project Lighthouse boot safety audit")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = LighthouseBootloader(ROOT).inspect()
    lighthouse = result["lighthouse"]

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print()
    print("=" * 72)
    print("Project Lighthouse")
    print("=" * 72)
    print(f"Version : {lighthouse['version']}")
    print(f"Status  : {lighthouse['status']}")
    print(f"Failed  : {len(lighthouse['failed'])}")
    print("=" * 72)


if __name__ == "__main__":
    main()
