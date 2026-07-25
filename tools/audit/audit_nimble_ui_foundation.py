from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "reports" / "nimble"
JSON_REPORT = REPORT_DIR / "nimble_ui_foundation_audit.json"
MARKDOWN_REPORT = REPORT_DIR / "nimble_ui_foundation_audit.md"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "archive",
    "quarantine",
    "restore_points",
    "reports",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "coverage",
}

FRONTEND_EXTENSIONS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".vue",
    ".svelte",
    ".astro",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".html",
}

MANIFEST_NAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
}

CONFIG_NAMES = {
    "vite.config.js",
    "vite.config.ts",
    "vite.config.mjs",
    "next.config.js",
    "next.config.mjs",
    "next.config.ts",
    "nuxt.config.js",
    "nuxt.config.ts",
    "astro.config.js",
    "astro.config.mjs",
    "svelte.config.js",
    "tailwind.config.js",
    "tailwind.config.ts",
    "postcss.config.js",
    "postcss.config.cjs",
    "tsconfig.json",
    "jsconfig.json",
    "components.json",
    "eslint.config.js",
    "eslint.config.mjs",
}

UI_DIRECTORY_NAMES = {
    "ui",
    "frontend",
    "web",
    "client",
    "app",
    "apps",
    "components",
    "pages",
    "routes",
    "views",
    "screens",
    "layouts",
    "styles",
    "theme",
    "themes",
    "design-system",
    "design_system",
    "dashboard",
    "dashboards",
}

ENTRYPOINT_NAMES = {
    "main.js",
    "main.jsx",
    "main.ts",
    "main.tsx",
    "index.js",
    "index.jsx",
    "index.ts",
    "index.tsx",
    "app.js",
    "app.jsx",
    "app.ts",
    "app.tsx",
    "layout.tsx",
    "page.tsx",
}

DEPENDENCY_GROUPS = {
    "frameworks": {
        "react",
        "react-dom",
        "next",
        "vue",
        "nuxt",
        "svelte",
        "@sveltejs/kit",
        "astro",
        "solid-js",
        "@angular/core",
    },
    "styling": {
        "tailwindcss",
        "styled-components",
        "@emotion/react",
        "@emotion/styled",
        "sass",
        "less",
        "postcss",
        "class-variance-authority",
        "clsx",
        "tailwind-merge",
    },
    "components": {
        "@radix-ui/react-dialog",
        "@radix-ui/react-dropdown-menu",
        "@radix-ui/react-popover",
        "@radix-ui/react-tabs",
        "@headlessui/react",
        "@mui/material",
        "@chakra-ui/react",
        "antd",
        "shadcn-ui",
    },
    "motion": {
        "framer-motion",
        "motion",
        "gsap",
        "@react-spring/web",
        "react-spring",
        "animejs",
        "lottie-react",
        "@lottiefiles/react-lottie-player",
    },
    "visualization": {
        "d3",
        "d3-force",
        "recharts",
        "chart.js",
        "react-chartjs-2",
        "echarts",
        "echarts-for-react",
        "vis-network",
        "cytoscape",
        "reactflow",
        "@xyflow/react",
        "three",
        "@react-three/fiber",
        "@react-three/drei",
    },
    "state": {
        "redux",
        "@reduxjs/toolkit",
        "zustand",
        "jotai",
        "recoil",
        "mobx",
        "xstate",
        "@tanstack/react-query",
        "swr",
    },
    "routing": {
        "react-router",
        "react-router-dom",
        "@tanstack/react-router",
    },
    "testing": {
        "vitest",
        "jest",
        "@testing-library/react",
        "@playwright/test",
        "cypress",
    },
    "accessibility": {
        "axe-core",
        "jest-axe",
        "@axe-core/playwright",
        "eslint-plugin-jsx-a11y",
    },
}


def is_excluded(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return True

    return any(part in EXCLUDED_DIRS for part in relative.parts)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def classify_dependencies(
    dependencies: dict[str, str],
) -> dict[str, list[str]]:
    classification: dict[str, list[str]] = {}

    for group, known_names in DEPENDENCY_GROUPS.items():
        matches = sorted(
            name
            for name in dependencies
            if name in known_names
        )
        if matches:
            classification[group] = matches

    return classification


def inspect_package_manifest(path: Path) -> dict[str, Any]:
    content = read_json(path)

    if content is None:
        return {
            "path": relative(path),
            "valid_json": False,
        }

    dependencies: dict[str, str] = {}

    for section in (
        "dependencies",
        "devDependencies",
        "peerDependencies",
        "optionalDependencies",
    ):
        values = content.get(section, {})
        if isinstance(values, dict):
            dependencies.update(values)

    scripts = content.get("scripts", {})
    if not isinstance(scripts, dict):
        scripts = {}

    workspaces = content.get("workspaces", [])
    if isinstance(workspaces, dict):
        workspaces = workspaces.get("packages", [])

    return {
        "path": relative(path),
        "valid_json": True,
        "name": content.get("name"),
        "version": content.get("version"),
        "private": content.get("private"),
        "package_manager": content.get("packageManager"),
        "workspaces": workspaces,
        "scripts": scripts,
        "dependency_count": len(dependencies),
        "dependency_groups": classify_dependencies(
            dependencies
        ),
        "all_dependencies": dict(
            sorted(dependencies.items())
        ),
    }


def discover_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not is_excluded(path)
    )


def discover_directories() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_dir() and not is_excluded(path)
    )


def detect_probable_routes(
    frontend_files: list[Path],
) -> list[str]:
    route_files: list[str] = []

    for path in frontend_files:
        parts_lower = {
            part.lower()
            for part in path.parts
        }

        if (
            {"pages", "routes", "screens", "views"}
            & parts_lower
        ):
            route_files.append(relative(path))
            continue

        if path.name.lower() in {
            "page.tsx",
            "page.jsx",
            "route.ts",
            "route.js",
        }:
            route_files.append(relative(path))

    return sorted(route_files)


def detect_component_files(
    frontend_files: list[Path],
) -> list[str]:
    components: list[str] = []

    for path in frontend_files:
        parts_lower = {
            part.lower()
            for part in path.parts
        }

        if "components" in parts_lower or "ui" in parts_lower:
            components.append(relative(path))

    return sorted(components)


def detect_style_files(
    frontend_files: list[Path],
) -> list[str]:
    return sorted(
        relative(path)
        for path in frontend_files
        if path.suffix.lower()
        in {
            ".css",
            ".scss",
            ".sass",
            ".less",
        }
    )


def detect_token_candidates(
    files: list[Path],
) -> list[str]:
    candidates: list[str] = []

    keywords = {
        "token",
        "tokens",
        "theme",
        "themes",
        "palette",
        "typography",
        "spacing",
        "colors",
        "variables",
    }

    for path in files:
        path_words = {
            part.lower()
            for part in path.parts
        }

        stem_words = set(
            path.stem.lower()
            .replace("-", "_")
            .split("_")
        )

        if keywords & (path_words | stem_words):
            candidates.append(relative(path))

    return sorted(candidates)


def build_report() -> dict[str, Any]:
    files = discover_files()
    directories = discover_directories()

    frontend_files = [
        path
        for path in files
        if path.suffix.lower()
        in FRONTEND_EXTENSIONS
    ]

    manifests = [
        path
        for path in files
        if path.name in MANIFEST_NAMES
    ]

    package_manifests = [
        path
        for path in manifests
        if path.name == "package.json"
    ]

    configs = [
        path
        for path in files
        if path.name in CONFIG_NAMES
    ]

    ui_directories = [
        path
        for path in directories
        if path.name.lower()
        in UI_DIRECTORY_NAMES
    ]

    entrypoints = [
        path
        for path in frontend_files
        if path.name.lower()
        in ENTRYPOINT_NAMES
    ]

    extension_counts = Counter(
        path.suffix.lower()
        for path in frontend_files
    )

    package_details = [
        inspect_package_manifest(path)
        for path in package_manifests
    ]

    detected_groups: dict[str, set[str]] = {}

    for package in package_details:
        for group, names in package.get(
            "dependency_groups",
            {},
        ).items():
            detected_groups.setdefault(
                group,
                set(),
            ).update(names)

    probable_roots = sorted(
        {
            relative(path.parent)
            for path in package_manifests
        }
        | {
            relative(path.parent)
            for path in configs
        }
        | {
            relative(path.parent)
            for path in entrypoints
        }
    )

    return {
        "repository_root": str(ROOT),
        "summary": {
            "active_files": len(files),
            "frontend_files": len(frontend_files),
            "package_manifests": len(package_manifests),
            "frontend_configs": len(configs),
            "ui_directories": len(ui_directories),
            "entrypoints": len(entrypoints),
            "probable_routes": len(
                detect_probable_routes(frontend_files)
            ),
            "component_files": len(
                detect_component_files(frontend_files)
            ),
            "style_files": len(
                detect_style_files(frontend_files)
            ),
            "token_candidates": len(
                detect_token_candidates(files)
            ),
        },
        "frontend_extension_counts": dict(
            sorted(extension_counts.items())
        ),
        "probable_frontend_roots": probable_roots,
        "package_manifests": package_details,
        "detected_dependency_groups": {
            group: sorted(names)
            for group, names
            in sorted(detected_groups.items())
        },
        "configuration_files": [
            relative(path)
            for path in configs
        ],
        "ui_directories": [
            relative(path)
            for path in ui_directories
        ],
        "entrypoints": [
            relative(path)
            for path in entrypoints
        ],
        "probable_routes": detect_probable_routes(
            frontend_files
        ),
        "component_files": detect_component_files(
            frontend_files
        ),
        "style_files": detect_style_files(
            frontend_files
        ),
        "token_candidates": detect_token_candidates(
            files
        ),
    }


def render_markdown(
    report: dict[str, Any],
) -> str:
    summary = report["summary"]

    lines = [
        "# Nimble™ UX Foundation Audit",
        "",
        "## Executive Summary",
        "",
        f"- Active files scanned: **{summary['active_files']}**",
        f"- Frontend-related files: **{summary['frontend_files']}**",
        f"- Package manifests: **{summary['package_manifests']}**",
        f"- Frontend configuration files: **{summary['frontend_configs']}**",
        f"- UI-related directories: **{summary['ui_directories']}**",
        f"- Entrypoints: **{summary['entrypoints']}**",
        f"- Probable route files: **{summary['probable_routes']}**",
        f"- Component files: **{summary['component_files']}**",
        f"- Style files: **{summary['style_files']}**",
        f"- Design-token candidates: **{summary['token_candidates']}**",
        "",
        "## Probable Frontend Roots",
        "",
    ]

    roots = report["probable_frontend_roots"]

    if roots:
        lines.extend(
            f"- `{root}`"
            for root in roots
        )
    else:
        lines.append(
            "- No canonical frontend root detected."
        )

    lines.extend(
        [
            "",
            "## Detected Technology",
            "",
        ]
    )

    groups = report["detected_dependency_groups"]

    if groups:
        for group, names in groups.items():
            lines.append(
                f"- **{group.title()}**: "
                + ", ".join(
                    f"`{name}`"
                    for name in names
                )
            )
    else:
        lines.append(
            "- No recognized frontend dependencies detected."
        )

    lines.extend(
        [
            "",
            "## Package Manifests",
            "",
        ]
    )

    for package in report["package_manifests"]:
        lines.append(
            f"### `{package['path']}`"
        )
        lines.append("")

        if not package.get("valid_json"):
            lines.append("- Invalid JSON")
            lines.append("")
            continue

        lines.extend(
            [
                f"- Name: `{package.get('name')}`",
                f"- Version: `{package.get('version')}`",
                f"- Dependencies: **{package.get('dependency_count', 0)}**",
                "",
            ]
        )

    sections = (
        (
            "Configuration Files",
            report["configuration_files"],
        ),
        (
            "UI Directories",
            report["ui_directories"],
        ),
        (
            "Entrypoints",
            report["entrypoints"],
        ),
        (
            "Probable Routes",
            report["probable_routes"],
        ),
        (
            "Component Files",
            report["component_files"],
        ),
        (
            "Style Files",
            report["style_files"],
        ),
        (
            "Design-Token Candidates",
            report["token_candidates"],
        ),
    )

    for title, entries in sections:
        lines.extend(
            [
                "",
                f"## {title}",
                "",
            ]
        )

        if entries:
            lines.extend(
                f"- `{entry}`"
                for entry in entries
            )
        else:
            lines.append("- None detected.")

    lines.extend(
        [
            "",
            "## Architectural Interpretation",
            "",
            "This report inventories the current active frontend surface.",
            "It does not designate a canonical frontend root.",
            "That decision should be made after reviewing duplication,",
            "framework consistency, route ownership, component reuse,",
            "motion support, accessibility, and design-token maturity.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report = build_report()

    JSON_REPORT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    MARKDOWN_REPORT.write_text(
        render_markdown(report),
        encoding="utf-8",
    )

    summary = report["summary"]

    print("=" * 72)
    print("NIMBLE™ UX FOUNDATION AUDIT")
    print("=" * 72)
    print(
        "Active files scanned:",
        summary["active_files"],
    )
    print(
        "Frontend files:",
        summary["frontend_files"],
    )
    print(
        "Package manifests:",
        summary["package_manifests"],
    )
    print(
        "Frontend configs:",
        summary["frontend_configs"],
    )
    print(
        "UI directories:",
        summary["ui_directories"],
    )
    print(
        "Entrypoints:",
        summary["entrypoints"],
    )
    print(
        "Probable routes:",
        summary["probable_routes"],
    )
    print(
        "Component files:",
        summary["component_files"],
    )
    print(
        "Style files:",
        summary["style_files"],
    )
    print(
        "Token candidates:",
        summary["token_candidates"],
    )
    print()
    print("Probable frontend roots:")

    roots = report["probable_frontend_roots"]

    if roots:
        for root in roots:
            print("  -", root)
    else:
        print("  - None detected")

    print()
    print(
        "Markdown report:",
        MARKDOWN_REPORT.relative_to(ROOT),
    )
    print(
        "JSON report:",
        JSON_REPORT.relative_to(ROOT),
    )


if __name__ == "__main__":
    main()
