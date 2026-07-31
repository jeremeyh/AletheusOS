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

SOURCE = ROOT / "nimble" / "design-tokens" / "source"
GENERATED = ROOT / "nimble" / "design-tokens" / "generated"

REQUIRED_SOURCE_FILES = [
    SOURCE / "primitives.json",
    SOURCE / "themes.json",
    SOURCE / "motion.json",
]

REQUIRED_GENERATED_FILES = [
    GENERATED / "nimble.tokens.css",
    GENERATED / "nimble.tokens.json",
    GENERATED / "nimble.tokens.ts",
]

REQUIRED_PRIMITIVE_GROUPS = {
    "color",
    "spacing",
    "radius",
    "opacity",
    "typography",
    "depth",
    "layout",
}

REQUIRED_SEMANTIC_GROUPS = {
    "surface",
    "text",
    "border",
    "brand",
    "status",
    "state",
}

REQUIRED_MOTION_GROUPS = {
    "duration",
    "easing",
    "spring",
    "distance",
    "scale",
    "reduced",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_scalar_leaves(
    value: Any,
    path: str,
) -> None:
    if isinstance(value, dict):
        if not value:
            raise ValueError(f"Empty token group: {path}")

        for key, child in value.items():
            assert_scalar_leaves(
                child,
                f"{path}.{key}",
            )
        return

    if not isinstance(value, (str, int, float, bool)):
        raise TypeError(f"Unsupported token value at {path}: {type(value).__name__}")


def main() -> None:
    missing = [
        path
        for path in (REQUIRED_SOURCE_FILES + REQUIRED_GENERATED_FILES)
        if not path.exists()
    ]

    if missing:
        for path in missing:
            print("MISSING:", path.relative_to(ROOT))
        raise SystemExit(1)

    primitives_document = load_json(SOURCE / "primitives.json")
    themes_document = load_json(SOURCE / "themes.json")
    motion_document = load_json(SOURCE / "motion.json")
    compiled_document = load_json(GENERATED / "nimble.tokens.json")

    primitive_groups = set(primitives_document) - {"meta"}

    missing_primitive_groups = REQUIRED_PRIMITIVE_GROUPS - primitive_groups

    if missing_primitive_groups:
        raise ValueError(
            "Missing primitive groups: " + ", ".join(sorted(missing_primitive_groups))
        )

    themes = themes_document.get("themes", {})

    if set(themes) != {"light", "dark"}:
        raise ValueError("Nimble must define exactly light and dark foundation themes.")

    for theme_name, theme in themes.items():
        missing_semantic_groups = REQUIRED_SEMANTIC_GROUPS - set(theme)

        if missing_semantic_groups:
            raise ValueError(
                f"{theme_name} missing semantic groups: "
                + ", ".join(sorted(missing_semantic_groups))
            )

        assert_scalar_leaves(
            theme,
            f"themes.{theme_name}",
        )

    motion = motion_document.get("motion", {})

    missing_motion_groups = REQUIRED_MOTION_GROUPS - set(motion)

    if missing_motion_groups:
        raise ValueError(
            "Missing motion groups: " + ", ".join(sorted(missing_motion_groups))
        )

    assert_scalar_leaves(
        {key: value for key, value in primitives_document.items() if key != "meta"},
        "primitives",
    )

    assert_scalar_leaves(
        motion,
        "motion",
    )

    if compiled_document.get("meta", {}).get("generated") is not True:
        raise ValueError("Compiled token document is not marked generated.")

    print("=" * 72)
    print("NIMBLE™ TOKEN VALIDATION")
    print("=" * 72)
    print(
        "Primitive groups:",
        len(primitive_groups),
    )
    print(
        "Semantic themes:",
        len(themes),
    )
    print(
        "Motion groups:",
        len(motion),
    )
    print("Generated outputs: 3")
    print("Status: PASS")


if __name__ == "__main__":
    main()
