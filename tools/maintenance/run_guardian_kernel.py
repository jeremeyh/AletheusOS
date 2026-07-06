import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "aletheus" / "runtime"

if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from guardian.kernel import GuardianKernel


def main():
    parser = argparse.ArgumentParser(description="Guardian Kernel™")
    parser.add_argument("--action", default="inspect")
    parser.add_argument("--target", default="")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--lockdown", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    kernel = GuardianKernel(ROOT)

    if args.status:
        result = kernel.status()
    elif args.lockdown:
        result = kernel.lockdown(reason=args.source)
    else:
        result = kernel.inspect(
            action=args.action,
            target=args.target,
            source=args.source,
        )

    if args.json:
        print(json.dumps(result, indent=2))
        return

    guardian = result["guardian"]
    decision = guardian.get("decision", {})

    print()
    print("=" * 72)
    print("Guardian Kernel™")
    print("=" * 72)
    print(f"Version : {guardian.get('version')}")
    print(f"Allowed : {decision.get('allowed')}")
    print(f"Mode    : {decision.get('mode', guardian.get('status'))}")
    print(f"Message : {decision.get('message', guardian.get('reason'))}")

    event = guardian.get("event")
    if event:
        print(f"Risk    : {event.get('risk')}")
        print(f"Target  : {event.get('target')}")
        print(f"Source  : {event.get('source')}")

    print("=" * 72)


if __name__ == "__main__":
    main()
