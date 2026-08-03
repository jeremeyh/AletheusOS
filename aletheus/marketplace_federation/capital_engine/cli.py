import json

from .engine import Engine


def main() -> int:
    _ = Engine()
    print(
        json.dumps(
            {
                "component": "Capital Commerce Engine",
                "version": "31.2.0",
                "status": "READY",
            },
            indent=2,
        )
    )
    return 0
