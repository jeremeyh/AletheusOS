from __future__ import annotations

from json import dumps

from .engine import Engine


def main() -> None:
    result = Engine().adapt({"state": "ACTIVE"}, {"confidence": 0.4})
    print(dumps(result, indent=2, sort_keys=True))
