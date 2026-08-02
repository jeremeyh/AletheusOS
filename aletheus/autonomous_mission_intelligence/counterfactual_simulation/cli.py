from __future__ import annotations

from json import dumps

from .engine import Engine


def main() -> None:
    result = Engine().simulate(
        [{"value": 10.0, "probability": 0.8, "cost": 2.0, "risk": 0.1}]
    )
    print(dumps(result, indent=2, sort_keys=True))
