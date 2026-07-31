from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import tomllib
from datetime import UTC, datetime
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

NIMBLE_PACKAGE = ROOT / "nimble" / "package.json"
NIMBLE_LOCK = ROOT / "nimble" / "package-lock.json"
PYPROJECT = ROOT / "pyproject.toml"

MANIFEST = ROOT / "nimble" / "governance" / "supply-chain" / "dependency-manifest.json"

REPORT = ROOT / "reports" / "nimble" / "dependency-manifest-latest.md"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def command_output(
    command: list[str],
    fallback: str = "unknown",
) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except FileNotFoundError:
        return fallback

    if completed.returncode != 0:
        return fallback

    value = completed.stdout.strip()
    return value or fallback


def collect_npm_dependencies() -> dict[str, Any]:
    package = json.loads(
        NIMBLE_PACKAGE.read_text(
            encoding="utf-8",
        )
    )

    lock = json.loads(
        NIMBLE_LOCK.read_text(
            encoding="utf-8",
        )
    )

    packages = lock.get("packages", {})
    resolved: list[dict[str, Any]] = []

    for package_path, metadata in sorted(packages.items()):
        if not package_path.startswith("node_modules/"):
            continue

        name = metadata.get("name")

        if not name:
            name = package_path.removeprefix("node_modules/")

        resolved.append(
            {
                "name": name,
                "version": metadata.get(
                    "version",
                    "unknown",
                ),
                "license": metadata.get(
                    "license",
                    "unknown",
                ),
                "integrity": metadata.get(
                    "integrity",
                ),
                "development": bool(metadata.get("dev", False)),
                "optional": bool(
                    metadata.get(
                        "optional",
                        False,
                    )
                ),
            }
        )

    return {
        "workspace": package.get(
            "name",
            "unknown",
        ),
        "lockfile_version": lock.get("lockfileVersion"),
        "direct_dependencies": package.get(
            "dependencies",
            {},
        ),
        "direct_dev_dependencies": package.get(
            "devDependencies",
            {},
        ),
        "resolved_package_count": len(resolved),
        "resolved_packages": resolved,
        "package_json_sha256": sha256_file(NIMBLE_PACKAGE),
        "package_lock_sha256": sha256_file(NIMBLE_LOCK),
    }


def collect_python_direct_dependencies() -> list[str]:
    if not PYPROJECT.exists():
        return []

    data = tomllib.loads(
        PYPROJECT.read_text(
            encoding="utf-8",
        )
    )

    project = data.get("project", {})

    dependencies = list(project.get("dependencies", []))

    optional = project.get(
        "optional-dependencies",
        {},
    )

    for group, values in sorted(optional.items()):
        for value in values:
            dependencies.append(f"{value} [optional:{group}]")

    return sorted(dependencies)


def collect_installed_python_packages() -> list[dict[str, str]]:
    packages: list[dict[str, str]] = []

    for distribution in sorted(
        importlib.metadata.distributions(),
        key=lambda item: item.metadata.get(
            "Name",
            "",
        ).lower(),
    ):
        name = distribution.metadata.get("Name")

        if not name:
            continue

        packages.append(
            {
                "name": name,
                "version": distribution.version,
                "license": distribution.metadata.get(
                    "License",
                    "unknown",
                )
                or "unknown",
            }
        )

    return packages


def git_metadata() -> dict[str, Any]:
    return {
        "commit": command_output(
            ["git", "rev-parse", "HEAD"],
        ),
        "short_commit": command_output(
            ["git", "rev-parse", "--short", "HEAD"],
        ),
        "branch": command_output(
            ["git", "branch", "--show-current"],
        ),
    }


def write_markdown(
    manifest: dict[str, Any],
) -> None:
    npm = manifest["npm"]
    python_data = manifest["python"]

    lines = [
        "# Nimble Dependency Manifest",
        "",
        f"Generated: `{manifest['generated_at']}`",
        f"Commit: `{manifest['source']['short_commit']}`",
        "",
        "## Node",
        "",
        f"- Runtime: `{manifest['runtime']['node']}`",
        f"- npm: `{manifest['runtime']['npm']}`",
        f"- Lockfile version: `{npm['lockfile_version']}`",
        (f"- Resolved packages: `{npm['resolved_package_count']}`"),
        (f"- package-lock SHA-256: `{npm['package_lock_sha256']}`"),
        "",
        "## Python",
        "",
        f"- Runtime: `{manifest['runtime']['python']}`",
        (
            "- Direct dependency declarations: "
            f"`{len(python_data['direct_dependencies'])}`"
        ),
        (f"- Installed distributions: `{python_data['installed_package_count']}`"),
        "",
        "## Direct Node dependencies",
        "",
        "| Package | Constraint | Type |",
        "|---|---|---|",
    ]

    for name, constraint in sorted(npm["direct_dependencies"].items()):
        lines.append(f"| `{name}` | `{constraint}` | runtime |")

    for name, constraint in sorted(npm["direct_dev_dependencies"].items()):
        lines.append(f"| `{name}` | `{constraint}` | development |")

    lines.extend(
        [
            "",
            "## Direct Python dependencies",
            "",
        ]
    )

    if python_data["direct_dependencies"]:
        for dependency in python_data["direct_dependencies"]:
            lines.append(f"- `{dependency}`")
    else:
        lines.append("- No PEP 621 project dependencies found.")

    REPORT.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    required = (
        NIMBLE_PACKAGE,
        NIMBLE_LOCK,
    )

    missing = [path for path in required if not path.exists()]

    if missing:
        for path in missing:
            print(
                "FAIL: Missing dependency source:",
                path.relative_to(ROOT),
            )
        return 1

    python_packages = collect_installed_python_packages()

    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "source": git_metadata(),
        "runtime": {
            "python": platform.python_version(),
            "python_executable": sys.executable,
            "node": command_output(
                ["node", "--version"],
            ),
            "npm": command_output(
                ["npm", "--version"],
            ),
            "platform": platform.platform(),
        },
        "npm": collect_npm_dependencies(),
        "python": {
            "pyproject_present": PYPROJECT.exists(),
            "pyproject_sha256": (
                sha256_file(PYPROJECT) if PYPROJECT.exists() else None
            ),
            "direct_dependencies": collect_python_direct_dependencies(),
            "installed_package_count": len(python_packages),
            "installed_packages": python_packages,
        },
    }

    MANIFEST.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    MANIFEST.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    write_markdown(manifest)

    print("=" * 72)
    print("NIMBLE™ DEPENDENCY MANIFEST")
    print("=" * 72)
    print(
        "Node packages:",
        manifest["npm"]["resolved_package_count"],
    )
    print(
        "Python packages:",
        manifest["python"]["installed_package_count"],
    )
    print(
        "Manifest:",
        MANIFEST.relative_to(ROOT),
    )
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
