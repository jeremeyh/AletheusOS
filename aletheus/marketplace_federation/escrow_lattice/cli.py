import json

from .engine import Engine


def main() -> int:
    _ = Engine()
    print(
        json.dumps(
            {"component": "Escrow Lattice", "version": "31.7.0", "status": "READY"},
            indent=2,
        )
    )
    return 0
