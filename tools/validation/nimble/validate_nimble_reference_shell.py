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

SHELL = ROOT / "nimble" / "reference-shell"

HTML = SHELL / "index.html"
CSS = SHELL / "assets" / "nimble-shell.css"
JS = SHELL / "assets" / "nimble-shell.js"
MANIFEST = SHELL / "shell.manifest.json"

REQUIRED_FILES = [
    HTML,
    CSS,
    JS,
    MANIFEST,
]

REQUIRED_HTML_MARKERS = [
    'id="nimble-main"',
    'data-action="open-command"',
    "data-command-dialog",
    'aria-label="Global navigation"',
    'aria-label="Context inspector"',
    'aria-live="polite"',
    "prefers-reduced-motion",
]

REQUIRED_JS_BEHAVIORS = [
    "toggleTheme",
    "toggleNavigation",
    "toggleInspector",
    "resetShell",
    "openCommand",
    "executeSelectedCommand",
    "localStorage",
]

REQUIRED_CSS_FEATURES = [
    "backdrop-filter",
    "@keyframes nimble-float",
    "@keyframes nimble-dialog-enter",
    "@media (prefers-reduced-motion: reduce)",
    "var(--nimble-semantic",
    "var(--nimble-motion",
]

REQUIRED_ENGINES = {
    "shell",
    "motion",
    "interaction",
    "workspace",
    "accessibility",
    "command",
    "transparency",
    "personalization",
}


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

    html = HTML.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    manifest = json.loads(
        MANIFEST.read_text(encoding="utf-8")
    )

    for marker in REQUIRED_HTML_MARKERS:
        if marker not in html and marker not in css:
            raise ValueError(
                f"Missing shell accessibility marker: {marker}"
            )

    for behavior in REQUIRED_JS_BEHAVIORS:
        if behavior not in js:
            raise ValueError(
                f"Missing shell behavior: {behavior}"
            )

    for feature in REQUIRED_CSS_FEATURES:
        if feature not in css:
            raise ValueError(
                f"Missing shell visual feature: {feature}"
            )

    implemented_engines = set(
        manifest["implemented_engines"]
    )

    missing_engines = (
        REQUIRED_ENGINES
        - implemented_engines
    )

    if missing_engines:
        raise ValueError(
            "Reference shell missing engines: "
            + ", ".join(sorted(missing_engines))
        )

    principle_x = manifest["principle_x"]

    concealed = [
        name
        for name, visible in principle_x.items()
        if visible is not True
    ]

    if concealed:
        raise ValueError(
            "Principle X violations: "
            + ", ".join(sorted(concealed))
        )

    accessibility = manifest["accessibility"]

    unsupported = [
        name
        for name, supported in accessibility.items()
        if supported is not True
    ]

    if unsupported:
        raise ValueError(
            "Accessibility requirements missing: "
            + ", ".join(sorted(unsupported))
        )

    print("=" * 72)
    print("NIMBLE™ REFERENCE SHELL VALIDATION")
    print("=" * 72)
    print("Rendered shell: present")
    print("Implemented engines:", len(implemented_engines))
    print(
        "Implemented surfaces:",
        len(manifest["implemented_surfaces"]),
    )
    print("Advanced motion: present")
    print("Command interaction: present")
    print("State persistence: present")
    print("Reduced motion: present")
    print("Principle X disclosure: active")
    print("Status: PASS")


if __name__ == "__main__":
    main()
