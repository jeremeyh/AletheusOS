"""
AletheusOS Import Doctor

Validates:
- Broken imports
- Syntax errors
- Missing __init__.py
- Duplicate module names
- Import timing
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))


IGNORED = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "build",
    "dist",
}


def discover_modules():

    modules = []

    for path in ROOT.rglob("*.py"):
        if any(part in IGNORED for part in path.parts):
            continue

        relative = path.relative_to(ROOT)

        module = ".".join(relative.with_suffix("").parts)

        modules.append(module)

    return sorted(modules)


def verify_import(module):

    start = time.perf_counter()

    try:
        importlib.import_module(module)

        elapsed = (time.perf_counter() - start) * 1000

        return True, elapsed, None

    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000

        return False, elapsed, str(e)


def check_missing_init():

    missing = []

    for directory in ROOT.rglob("*"):
        if not directory.is_dir():
            continue

        if any(part in IGNORED for part in directory.parts):
            continue

        py_files = list(directory.glob("*.py"))

        if not py_files:
            continue

        init = directory / "__init__.py"

        if not init.exists():
            missing.append(directory.relative_to(ROOT))

    return missing


def duplicate_modules(modules):

    seen = {}

    duplicates = {}

    for module in modules:
        short = module.split(".")[-1]

        if short in seen:
            duplicates.setdefault(short, []).append(module)

        else:
            seen[short] = module

    return duplicates


def main():

    print("=" * 70)
    print("AletheusOS Import Doctor")
    print("=" * 70)

    modules = discover_modules()

    failures = []

    success = 0

    total_time = 0

    for module in modules:
        ok, elapsed, error = verify_import(module)

        total_time += elapsed

        if ok:
            success += 1

            print(f"[ OK ] {module:<55} {elapsed:6.1f} ms")

        else:
            failures.append((module, error))

            print(f"[FAIL] {module}")

            print(f"       {error}")

    print()

    print("=" * 70)

    print(f"Modules checked : {len(modules)}")

    print(f"Successful      : {success}")

    print(f"Failures        : {len(failures)}")

    print(f"Import time     : {total_time:.1f} ms")

    print("=" * 70)

    missing = check_missing_init()

    if missing:
        print()

        print("Missing __init__.py")

        for item in missing:
            print(f"  - {item}")

    duplicates = duplicate_modules(modules)

    if duplicates:
        print()

        print("Duplicate Module Names")

        for name, items in duplicates.items():
            print()

            print(name)

            for m in items:
                print("   ", m)

    if failures:
        print()

        print("=" * 70)

        print("FAILED IMPORTS")

        print("=" * 70)

        for module, error in failures:
            print()

            print(module)

            print(error)

        raise SystemExit(1)

    print()

    print("✓ Import Doctor passed.")


if __name__ == "__main__":
    main()
