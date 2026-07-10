#!/bin/bash

set -euo pipefail

REPORT_DIR="reports/genesis_7_architecture_audit"
mkdir -p "$REPORT_DIR"

echo "Generating AletheusOS architecture inventory..."

find aletheus \
    -type f \
    \( \
        -name "*.py" \
        -o -name "*.json" \
        -o -name "*.yaml" \
        -o -name "*.yml" \
        -o -name "*.md" \
    \) \
    | sort \
    > "$REPORT_DIR/files.txt"

find aletheus \
    -type d \
    | sort \
    > "$REPORT_DIR/directories.txt"

grep -RIn \
    --include="*.py" \
    -E "^class |^def |^[[:space:]]+def " \
    aletheus \
    > "$REPORT_DIR/python_symbols.txt" || true

grep -RIn \
    --include="*.py" \
    -E '"range"[[:space:]]*:|'\''range'\''[[:space:]]*:' \
    aletheus \
    > "$REPORT_DIR/post_genesis_ranges.txt" || true

grep -RIn \
    --include="*.py" \
    -E "Principle X|Unconcealed Truth|Breadth|Guardian|Atlas|Watch Tower|Sentinel|Council|THOR|Mnemonic Cerebrum|MCC|SPA|Spectrum Platform Analyzer" \
    aletheus \
    > "$REPORT_DIR/constitutional_references.txt" || true

grep -RIn \
    --include="*.py" \
    -E "register|registry|initialize|startup|shutdown|health|dependency|lifecycle" \
    aletheus \
    > "$REPORT_DIR/runtime_references.txt" || true

find . \
    -maxdepth 3 \
    -type f \
    \( \
        -name "*.md" \
        -o -name "*.txt" \
        -o -name "*.yaml" \
        -o -name "*.yml" \
        -o -name "*.json" \
    \) \
    | sort \
    > "$REPORT_DIR/documentation_inventory.txt"

python - <<'PY' > "$REPORT_DIR/import_probe.txt"
from __future__ import annotations

import importlib
from pathlib import Path

print("AletheusOS import probe")
print("=" * 72)

package_root = Path("aletheus")
module_names: set[str] = set()

for path in package_root.rglob("*.py"):
    relative = path.relative_to(package_root)

    if relative.name == "__init__.py":
        if relative.parent == Path("."):
            module_names.add("aletheus")
        else:
            module_names.add(
                "aletheus." + ".".join(relative.parent.parts)
            )
    else:
        module_names.add(
            "aletheus."
            + ".".join(relative.with_suffix("").parts)
        )

failures: list[tuple[str, str, str]] = []

for name in sorted(module_names):
    try:
        importlib.import_module(name)
        print(f"PASS  {name}")
    except BaseException as exc:
        error_type = type(exc).__name__
        message = str(exc)

        failures.append(
            (
                name,
                error_type,
                message,
            )
        )

        print(
            f"FAIL  {name}: "
            f"{error_type}: {message}"
        )

print()
print("=" * 72)
print(f"Modules examined: {len(module_names)}")
print(f"Failures: {len(failures)}")

if failures:
    print()
    print("Failure summary")
    print("-" * 72)

    for name, error_type, message in failures:
        print(
            f"{name}\t{error_type}\t{message}"
        )
PY

echo
echo "Inventory complete:"
echo "$REPORT_DIR"
