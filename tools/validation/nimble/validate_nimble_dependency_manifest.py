from __future__ import annotations

import hashlib
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


MANIFEST = ROOT / "nimble" / "governance" / "supply-chain" / "dependency-manifest.json"

NIMBLE_PACKAGE = ROOT / "nimble" / "package.json"
NIMBLE_LOCK = ROOT / "nimble" / "package-lock.json"
PYPROJECT = ROOT / "pyproject.toml"

REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "generated_at",
    "source",
    "runtime",
    "npm",
    "python",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    if not MANIFEST.exists():
        print("FAIL: Dependency manifest is missing.")
        return 1

    data: dict[str, Any] = json.loads(MANIFEST.read_text(encoding="utf-8"))

    missing = REQUIRED_TOP_LEVEL_KEYS - set(data)

    if missing:
        print(
            "FAIL: Missing manifest keys:",
            ", ".join(sorted(missing)),
        )
        return 1

    npm = data["npm"]
    python_data = data["python"]

    if npm["package_json_sha256"] != sha256_file(NIMBLE_PACKAGE):
        print("FAIL: nimble/package.json changed without regenerating the manifest.")
        return 1

    if npm["package_lock_sha256"] != sha256_file(NIMBLE_LOCK):
        print(
            "FAIL: nimble/package-lock.json changed without regenerating the manifest."
        )
        return 1

    if PYPROJECT.exists():
        if python_data["pyproject_sha256"] != sha256_file(PYPROJECT):
            print(
                "FAIL: pyproject.toml changed without "
                "regenerating the dependency manifest."
            )
            return 1

    if npm["resolved_package_count"] != len(npm["resolved_packages"]):
        print("FAIL: Node package count does not match the package inventory.")
        return 1

    if python_data["installed_package_count"] != len(python_data["installed_packages"]):
        print("FAIL: Python package count does not match the package inventory.")
        return 1

    node_names = [package["name"] for package in npm["resolved_packages"]]

    if len(node_names) != len(set(node_names)):
        print("FAIL: Duplicate Node package records found.")
        return 1

    print("=" * 72)
    print("NIMBLE™ DEPENDENCY MANIFEST VALIDATION")
    print("=" * 72)
    print("package.json hash: valid")
    print("package-lock.json hash: valid")
    print(
        "Resolved Node packages:",
        npm["resolved_package_count"],
    )
    print(
        "Installed Python packages:",
        python_data["installed_package_count"],
    )
    print("Dependency inventory: consistent")
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
