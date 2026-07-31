from __future__ import annotations

import json
from pathlib import Path
from typing import Any


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

TAXONOMY_PATH = NIMBLE / "components" / "component_taxonomy.json"

SCHEMA_PATH = NIMBLE / "components" / "component_contract.schema.json"

CONTRACTS_PATH = NIMBLE / "components" / "core_component_contracts.json"

INTERACTION_PATH = NIMBLE / "interaction" / "interaction_contracts.json"

WORKSPACE_PATH = NIMBLE / "workspace" / "workspace_contracts.json"

REQUIRED_FILES = [
    TAXONOMY_PATH,
    SCHEMA_PATH,
    CONTRACTS_PATH,
    INTERACTION_PATH,
    WORKSPACE_PATH,
    NIMBLE / "interaction" / "INTERACTION_GRAMMAR.md",
    NIMBLE / "accessibility" / "ACCESSIBILITY_STANDARD.md",
]

REQUIRED_COMPONENT_FIELDS = {
    "name",
    "category",
    "role",
    "states",
    "interactions",
    "accessibility",
    "motion",
    "principle_x",
}

REQUIRED_PRINCIPLE_X_FIELDS = {
    "state_visible",
    "failure_visible",
    "reversibility_visible",
}

REQUIRED_ACCESSIBILITY_FIELDS = {
    "keyboard",
    "focus",
    "semantic_role",
    "reduced_motion",
}

REQUIRED_INTERACTIONS = {
    "activate",
    "drag",
    "resize",
    "dock",
    "execute",
    "navigate",
    "inspect",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_component(
    component: dict[str, Any],
    categories: set[str],
) -> None:
    missing = REQUIRED_COMPONENT_FIELDS - set(component)

    if missing:
        raise ValueError(
            f"{component.get('name', '<unknown>')} "
            f"missing fields: {', '.join(sorted(missing))}"
        )

    if component["category"] not in categories:
        raise ValueError(
            f"{component['name']} has unknown category: {component['category']}"
        )

    accessibility = component["accessibility"]

    missing_accessibility = REQUIRED_ACCESSIBILITY_FIELDS - set(accessibility)

    if missing_accessibility:
        raise ValueError(
            f"{component['name']} missing accessibility fields: "
            + ", ".join(sorted(missing_accessibility))
        )

    if accessibility["keyboard"] is not True:
        raise ValueError(f"{component['name']} must support keyboard access.")

    if accessibility["focus"] is not True:
        raise ValueError(f"{component['name']} must expose focus.")

    if accessibility["reduced_motion"] is not True:
        raise ValueError(f"{component['name']} must support reduced motion.")

    principle_x = component["principle_x"]

    missing_principle_x = REQUIRED_PRINCIPLE_X_FIELDS - set(principle_x)

    if missing_principle_x:
        raise ValueError(
            f"{component['name']} missing Principle X fields: "
            + ", ".join(sorted(missing_principle_x))
        )

    if principle_x["state_visible"] is not True:
        raise ValueError(f"{component['name']} conceals state.")

    if principle_x["failure_visible"] is not True:
        raise ValueError(f"{component['name']} conceals failure.")

    motion = component["motion"]

    if motion.get("interruptible") is not True:
        raise ValueError(f"{component['name']} motion must be interruptible.")

    if not motion.get("reduced_motion_fallback"):
        raise ValueError(f"{component['name']} requires a reduced-motion fallback.")


def main() -> None:
    missing_files = [path for path in REQUIRED_FILES if not path.exists()]

    if missing_files:
        for path in missing_files:
            print("MISSING:", path.relative_to(ROOT))
        raise SystemExit(1)

    taxonomy = load_json(TAXONOMY_PATH)
    contracts = load_json(CONTRACTS_PATH)
    interactions = load_json(INTERACTION_PATH)
    workspace = load_json(WORKSPACE_PATH)

    categories = set(taxonomy["categories"])

    components = contracts["components"]

    if not components:
        raise ValueError("No Nimble component contracts were defined.")

    names: set[str] = set()

    for component in components:
        name = component["name"]

        if name in names:
            raise ValueError(f"Duplicate component contract: {name}")

        names.add(name)
        validate_component(
            component,
            categories,
        )

    interaction_names = set(interactions["contracts"])

    missing_interactions = REQUIRED_INTERACTIONS - interaction_names

    if missing_interactions:
        raise ValueError(
            "Missing interaction contracts: " + ", ".join(sorted(missing_interactions))
        )

    workspace_required = set(workspace["workspace"]["required_capabilities"])

    for capability in (
        "keyboard_navigation",
        "reduced_motion",
        "layout_persistence",
    ):
        if capability not in workspace_required:
            raise ValueError(f"Workspace missing required capability: {capability}")

    print("=" * 72)
    print("NIMBLE™ COMPONENT FOUNDATION VALIDATION")
    print("=" * 72)
    print("Component categories:", len(categories))
    print("Component contracts:", len(components))
    print("Interaction contracts:", len(interaction_names))
    print(
        "Workspace capabilities:",
        len(workspace_required),
    )
    print("Accessibility standard: present")
    print("Principle X enforcement: active")
    print("Status: PASS")


if __name__ == "__main__":
    main()
