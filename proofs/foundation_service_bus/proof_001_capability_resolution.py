from __future__ import annotations

from pprint import pprint

from aletheus.foundation_service_bus import foundation_service_bus


def main() -> None:
    print("FOUNDATION SERVICE BUS v1.0 PROOF")
    print("=" * 50)

    for requested in ["appraisal", "appraiserx", "valuation", "thorx", "marketplace", "unknown"]:
        resolution = foundation_service_bus.resolve(requested)
        print()
        print(f"REQUEST: {requested}")
        pprint(resolution.to_dict())

    print()
    print("APPRAISERᵡ PLAN")
    plan = foundation_service_bus.plan("appraiserx")
    pprint(plan.to_dict() if plan else None)

    print()
    print("HEALTH")
    pprint(foundation_service_bus.health())


if __name__ == "__main__":
    main()
