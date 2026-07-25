from __future__ import annotations

import json
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)

NIMBLE = ROOT / "nimble"

REQUIRED_FILES = [
    NIMBLE / "nimble.manifest.json",
    NIMBLE / "architecture" / "NIMBLE_ARCHITECTURE.md",
    NIMBLE / "architecture" / "engine_contracts.json",
    NIMBLE / "design-tokens" / "token.schema.json",
    NIMBLE / "motion" / "MOTION_CONSTITUTION.md",
    NIMBLE / "applications" / "application_inheritance.json",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    missing = [
        path
        for path in REQUIRED_FILES
        if not path.exists()
    ]

    if missing:
        for path in missing:
            print("MISSING:", path.relative_to(ROOT))
        raise SystemExit(1)

    manifest = read_json(
        NIMBLE / "nimble.manifest.json"
    )
    contracts = read_json(
        NIMBLE / "architecture" / "engine_contracts.json"
    )
    inheritance = read_json(
        NIMBLE / "applications" / "application_inheritance.json"
    )
    schema = read_json(
        NIMBLE / "design-tokens" / "token.schema.json"
    )

    required_engines = set(manifest["engines"])
    contract_engines = set(contracts)

    missing_contracts = required_engines - contract_engines

    if missing_contracts:
        print(
            "Missing engine contracts:",
            ", ".join(sorted(missing_contracts)),
        )
        raise SystemExit(1)

    required_inheritance = inheritance[
        "required_inheritance"
    ]

    disabled = [
        name
        for name, enabled in required_inheritance.items()
        if enabled is not True
    ]

    if disabled:
        print(
            "Disabled required inheritance:",
            ", ".join(sorted(disabled)),
        )
        raise SystemExit(1)

    token_requirements = set(schema["required"])
    expected_tokens = {
        "color",
        "typography",
        "spacing",
        "radius",
        "depth",
        "motion",
        "opacity",
        "layout",
    }

    if token_requirements != expected_tokens:
        print("Token schema requirements are incomplete.")
        raise SystemExit(1)

    print("=" * 72)
    print("NIMBLE™ FOUNDATION VALIDATION")
    print("=" * 72)
    print("Manifest: valid")
    print("Engine contracts: valid")
    print("Application inheritance: valid")
    print("Token schema: valid")
    print("Required engines:", len(required_engines))
    print("Status: PASS")


if __name__ == "__main__":
    main()
