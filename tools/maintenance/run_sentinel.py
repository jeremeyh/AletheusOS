import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "aletheus" / "runtime"

if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from sentinel.engine import SentinelEngine


def main():
    parser = argparse.ArgumentParser(description="Sentinel™ runtime health supervisor")
    parser.add_argument("--heartbeat", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    engine = SentinelEngine(ROOT)
    result = engine.heartbeat() if args.heartbeat else engine.scan()

    if args.json:
        print(json.dumps(result, indent=2))
        return

    sentinel = result["sentinel"]

    print()
    print("=" * 72)
    print("Sentinel™")
    print("=" * 72)
    print(f"Version      : {sentinel.get('version')}")
    print(f"Status       : {sentinel.get('status')}")
    print(f"Score        : {sentinel.get('score')}")
    print(f"Guardian Req : {sentinel.get('guardian_requested')}")
    print(f"WatchTower   : {sentinel.get('watch_tower_requested')}")
    print("=" * 72)


if __name__ == "__main__":
    main()
