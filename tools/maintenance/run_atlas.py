import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aletheus.atlas import AtlasEngine


def main():
    parser = argparse.ArgumentParser(description="Atlas™ architecture graph scanner")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = AtlasEngine(ROOT).inspect()
    atlas = result["atlas"]

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print()
    print("=" * 72)
    print("Atlas™")
    print("=" * 72)
    print(f"Version      : {atlas['version']}")
    print(f"Status       : {atlas['status']}")
    print(f"Score        : {atlas['score']}")
    print(f"Modules      : {atlas['summary']['modules']}")
    print(f"Imports      : {atlas['summary']['imports']}")
    print(f"Local Edges  : {atlas['summary']['local_edges']}")
    print(f"Cycles       : {atlas['summary']['cycles']}")
    print(f"Duplicates   : {atlas['summary']['duplicate_families']}")
    print("=" * 72)


if __name__ == "__main__":
    main()
