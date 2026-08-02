import json

from .engine import Engine


def main() -> int:
    _ = Engine()
    print(
        json.dumps(
            {"component": "SPARTAN Marketplace Security", "version": "31.12.0", "status": "READY"},
            indent=2,
        )
    )
    return 0
