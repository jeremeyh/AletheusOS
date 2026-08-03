from __future__ import annotations

from json import dumps

from .engine import Engine


def main() -> None:
    result = Engine().execute({"objective": "Genesis 34 decision demonstration"})
    print(dumps(result, indent=2, sort_keys=True))
