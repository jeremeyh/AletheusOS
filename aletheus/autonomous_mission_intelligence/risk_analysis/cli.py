from __future__ import annotations

from json import dumps

from .engine import Engine


def main() -> None:
    result = Engine().analyze({"operational": 0.2, "security": 0.1})
    print(dumps(result, indent=2, sort_keys=True))
