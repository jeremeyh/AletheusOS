import json

from .engine import Engine


def main() -> int:
    _ = Engine()
    print(
        json.dumps(
            {"component": "Trade Graph and Cycle Solver", "version": "31.8.0", "status": "READY"},
            indent=2,
        )
    )
    return 0
