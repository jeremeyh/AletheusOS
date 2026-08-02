from __future__ import annotations

from json import dumps

from .engine import Engine
from .models import MissionSpec


def main() -> None:
    mission = MissionSpec(
        mission_id="mission-demo",
        objective="Find and evaluate a bounded opportunity",
        domain="CARD_HAWK",
        budget=1500.0,
        priority=80,
    )
    print(dumps(Engine().evaluate(mission), default=str, indent=2))


if __name__ == "__main__":
    main()
