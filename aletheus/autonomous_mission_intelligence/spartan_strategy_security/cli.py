from __future__ import annotations

from json import dumps

from .engine import Engine


def main() -> None:
    result = Engine().inspect({"plan": "bounded"})
    print(dumps(result, indent=2, sort_keys=True))
