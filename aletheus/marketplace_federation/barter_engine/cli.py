import json

from .engine import Engine


def main() -> int:
    _ = Engine()
    print(
        json.dumps(
            {
                "component": "Barter Transaction Engine",
                "version": "31.3.0",
                "status": "READY",
            },
            indent=2,
        )
    )
    return 0
