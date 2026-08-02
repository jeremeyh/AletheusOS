from __future__ import annotations

from json import dumps

from .engine import Engine


def main() -> None:
    result = Engine().route("request-1", 0.6, ["owner@example.com"])
    print(dumps(result, indent=2, sort_keys=True))
