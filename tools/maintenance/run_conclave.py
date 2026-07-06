import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "aletheus" / "runtime"

if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from conclave import ConclaveEngine


def main():
    parser = argparse.ArgumentParser(description="Conclave™ defensive runtime shield")
    parser.add_argument("--action", default="inspect")
    parser.add_argument("--target", default="")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--lockdown", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    engine = ConclaveEngine(ROOT)

    if args.lockdown:
        result = engine.emergency_lockdown(reason=args.source)
    else:
        result = engine.protect(
            action=args.action,
            target=args.target,
            source=args.source,
        )

    if args.json:
        print(json.dumps(result, indent=2))
        return

    conclave = result["conclave"]

    print()
    print("=" * 72)
    print("Conclave™")
    print("=" * 72)
    print(f"Risk        : {conclave.get('risk', conclave.get('status'))}")
    print(f"Allowed     : {conclave.get('allowed', False)}")
    print(f"Shield      : {conclave.get('shield_engaged', conclave.get('status'))}")
    print(f"Principle X : {conclave.get('principle_x')}")
    print(f"Watch Tower : {conclave.get('watch_tower_requested')}")
    print(f"Response    : {conclave.get('response', conclave.get('message'))}")
    print("=" * 72)


if __name__ == "__main__":
    main()