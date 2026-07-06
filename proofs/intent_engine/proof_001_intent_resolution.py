from __future__ import annotations

from pprint import pprint

from aletheus.foundation_service_bus import foundation_service_bus
from aletheus.intent_engine import intent_engine


def main() -> None:
    print("INTENT ENGINE v1.0 PROOF")
    print("=" * 50)

    queries = [
        "What is my Caleb Williams Bowman worth?",
        "Should I sell my Matas Buzelis collection?",
        "Find recent comps for Rome Odunze autos.",
        "Analyze this asset.",
    ]

    for query in queries:
        print()
        print(f"QUERY: {query}")

        intent = intent_engine.resolve(
            identity="identity.founder.master_lord_6ixth",
            application="CardHawk",
            query=query,
        )

        pprint(intent.to_dict())

        print()
        print("FOUNDATION RESOLUTION")
        resolution = foundation_service_bus.resolve(intent.capability_request)
        pprint(resolution.to_dict())

    print()
    print("HEALTH")
    pprint(intent_engine.health())

    print()
    print("STATISTICS")
    pprint(intent_engine.statistics())


if __name__ == "__main__":
    main()
