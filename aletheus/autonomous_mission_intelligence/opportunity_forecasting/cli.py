from __future__ import annotations

from json import dumps

from .engine import Engine


def main() -> None:
    result = Engine().forecast([1.0, 2.0, 3.0])
    print(dumps(result, indent=2, sort_keys=True))
