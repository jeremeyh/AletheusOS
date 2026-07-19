#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "reports/nimble/experience/frontend-discovery.json"

IGNORED = {
    ".git",
    ".venv",
    "node_modules",
    "dist",
    "build",
    ".next",
    "coverage",
    "__pycache__",
}

PACKAGE_FILES = {
    "package.json",
    "pnpm-workspace.yaml",
    "yarn.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "vite.config.ts",
    "vite.config.js",
    "next.config.js",
    "next.config.mjs",
    "next.config.ts",
    "tsconfig.json",
}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_package(path: Path) -> dict[str, Any]:
    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError):
        return {}


def main() -> int:
    discovered_files: list[str] = []
    packages: list[dict[str, Any]] = []
    source_directories: set[str] = set()
    likely_ui_roots: set[str] = set()

    for path in ROOT.rglob("*"):
        if any(part in IGNORED for part in path.parts):
            continue

        if path.is_file() and path.name in PACKAGE_FILES:
            discovered_files.append(relative(path))

        if path.is_file() and path.name == "package.json":
            package = load_package(path)
            dependencies = {
                **package.get("dependencies", {}),
                **package.get("devDependencies", {}),
            }

            frameworks = sorted(
                name
                for name in [
                    "react",
                    "next",
                    "vite",
                    "@storybook/react",
                    "@storybook/react-vite",
                    "tailwindcss",
                    "@radix-ui/react-slot",
                    "styled-components",
                    "@emotion/react",
                ]
                if name in dependencies
            )

            package_root = path.parent

            packages.append(
                {
                    "path": relative(path),
                    "name": package.get("name"),
                    "private": package.get("private"),
                    "frameworks": frameworks,
                    "scripts": package.get("scripts", {}),
                }
            )

            if frameworks:
                likely_ui_roots.add(
                    relative(package_root)
                )

        if path.is_dir() and path.name in {
            "src",
            "app",
            "components",
            "ui",
            "styles",
            "theme",
            "tokens",
        }:
            source_directories.add(relative(path))

    report = {
        "schema_version": "1.0",
        "package_managers": {
            "npm": (ROOT / "package-lock.json").exists(),
            "pnpm": (ROOT / "pnpm-lock.yaml").exists(),
            "yarn": (ROOT / "yarn.lock").exists(),
        },
        "workspace_files": sorted(discovered_files),
        "packages": sorted(
            packages,
            key=lambda item: item["path"],
        ),
        "likely_ui_roots": sorted(likely_ui_roots),
        "source_directories": sorted(source_directories),
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ FRONTEND DISCOVERY")
    print("=" * 72)
    print(
        "Package managers:",
        ", ".join(
            name
            for name, present
            in report["package_managers"].items()
            if present
        )
        or "none detected",
    )
    print(
        "Package manifests:",
        len(packages),
    )
    print(
        "Likely UI roots:",
        len(likely_ui_roots),
    )

    for root in sorted(likely_ui_roots):
        print(f"- {root}")

    print(f"Report: {relative(REPORT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
