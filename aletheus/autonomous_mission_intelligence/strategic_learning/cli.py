from __future__ import annotations

from json import dumps

from .engine import Engine


def main() -> None:
    result = Engine().learn(0.5, 0.4, 0.8)
    print(dumps(result, indent=2, sort_keys=True))
