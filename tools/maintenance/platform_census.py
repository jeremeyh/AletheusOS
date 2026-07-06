from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALETHEUS = ROOT / "aletheus"
REPORT_DIR = ROOT / "reports" / "platform_census"


CATEGORY_HINTS = {
    "governance": ["council", "constitution", "principle", "governance"],
    "core_platform": ["runtime", "kernel", "platform", "orchestrator", "executive_kernel", "contracts"],
    "platform_service": ["guardian", "sentinel", "atlas", "archivist", "watch", "observer", "communications"],
    "engine": ["thor", "def", "soar", "perch", "eye", "oracle", "prediction", "reasoning", "decision"],
    "application": ["applications", "cardhawk"],
    "memory_knowledge": ["memory", "knowledge", "semantic", "learning"],
    "workflow": ["mission", "workflow", "planning", "agents", "copilot"],
    "infrastructure": ["security", "telemetry", "persistence", "plugins", "federation", "tenancy", "mesh"],
}


def classify(name: str) -> str:
    lowered = name.lower()

    for category, hints in CATEGORY_HINTS.items():
        if any(hint in lowered for hint in hints):
            return category

    return "unclassified"


def file_count(path: Path) -> int:
    return sum(1 for item in path.rglob("*") if item.is_file() and "__pycache__" not in item.parts)


def py_count(path: Path) -> int:
    return sum(1 for item in path.rglob("*.py") if "__pycache__" not in item.parts)


def has_contract_language(path: Path) -> bool:
    for file in path.rglob("*.py"):
        if "__pycache__" in file.parts:
            continue

        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if "PlatformContract" in text or "health(" in text or "statistics(" in text:
            return True

    return False


def inspect_package(path: Path) -> dict:
    init = path / "__init__.py"

    return {
        "name": path.name,
        "path": path.relative_to(ROOT).as_posix(),
        "category": classify(path.name),
        "has_init": init.exists(),
        "files": file_count(path),
        "python_files": py_count(path),
        "has_contract_language": has_contract_language(path),
    }


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    packages = []

    for item in sorted(ALETHEUS.iterdir()):
        if not item.is_dir():
            continue

        if item.name == "__pycache__":
            continue

        packages.append(inspect_package(item))

    by_category = {}

    for package in packages:
        by_category.setdefault(package["category"], []).append(package["name"])

    result = {
        "platform_census": {
            "generated_at": datetime.utcnow().isoformat(),
            "root": str(ROOT),
            "aletheus_packages": len(packages),
            "categories": by_category,
            "packages": packages,
        }
    }

    json_path = REPORT_DIR / "platform_census.json"
    md_path = REPORT_DIR / "platform_census.md"

    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    md_path.write_text(markdown(result), encoding="utf-8")

    print("AletheusOS Platform Census")
    print("=" * 40)
    print(f"Packages: {len(packages)}")
    print()

    for category, names in sorted(by_category.items()):
        print(f"{category}: {len(names)}")
        for name in names:
            print(f"  - {name}")
        print()

    print(f"Report: {json_path}")
    print(f"Report: {md_path}")


def markdown(result: dict) -> str:
    census = result["platform_census"]

    lines = [
        "# AletheusOS Platform Census",
        "",
        f"Generated: {census['generated_at']}",
        f"Packages: {census['aletheus_packages']}",
        "",
        "## Categories",
        "",
    ]

    for category, names in sorted(census["categories"].items()):
        lines.append(f"### {category}")
        lines.append("")
        for name in names:
            lines.append(f"- {name}")
        lines.append("")

    lines.append("## Package Details")
    lines.append("")

    for package in census["packages"]:
        lines.extend([
            f"### {package['name']}",
            "",
            f"- Path: `{package['path']}`",
            f"- Category: `{package['category']}`",
            f"- Has `__init__.py`: `{package['has_init']}`",
            f"- Files: `{package['files']}`",
            f"- Python files: `{package['python_files']}`",
            f"- Contract language detected: `{package['has_contract_language']}`",
            "",
        ])

    return "\n".join(lines)


if __name__ == "__main__":
    main()
