import json

from .engine import Engine


def main() -> int:
    _ = Engine()
    print(
        json.dumps(
            {"component": "Commerce Value Abstraction", "version": "31.5.0", "status": "READY"},
            indent=2,
        )
    )
    return 0
