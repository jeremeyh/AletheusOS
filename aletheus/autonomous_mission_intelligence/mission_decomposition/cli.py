from __future__ import annotations

from json import dumps

from .engine import Engine
from .models import (
    StrategicObjective,
)


def main() -> None:
    objective = StrategicObjective(
        "objective-demo", "Demonstrate Mission Decomposition Engine"
    )
    result = Engine().decompose(objective)
    print(dumps(result, indent=2, sort_keys=True))
