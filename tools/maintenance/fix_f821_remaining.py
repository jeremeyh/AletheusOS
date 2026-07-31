#!/usr/bin/env python3
"""
Genesis 11
F821 Remaining Repair Script

Repairs the remaining intentional F821 findings:

1. Adds `import streamlit as st` if missing.
2. Removes stray `s[3]`.
3. Fixes SAFE_COMMAND_ALIASES reference.
4. Repairs archived session reference (or annotates for manual review).

Safe to run multiple times.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def patch_streamlit():
    path = ROOT / "archives/prototypes/founder_console_runtime_v2.py"

    if not path.exists():
        print("SKIP:", path)
        return

    text = path.read_text()

    if "import streamlit as st" not in text:
        lines = text.splitlines()

        insert_at = 0

        if lines and lines[0].startswith("#!"):
            insert_at = 1

        while insert_at < len(lines):
            stripped = lines[insert_at].strip()

            if (
                stripped.startswith('"""')
                or stripped.startswith("'''")
                or stripped == ""
            ):
                insert_at += 1
                continue

            break

        lines.insert(insert_at, "import streamlit as st")
        text = "\n".join(lines)

        path.write_text(text)
        print("FIXED:", path.name, "(added streamlit import)")
    else:
        print("OK:", path.name)


def patch_validation():
    path = ROOT / "tools/validation/nimble/validate_nimble_audit_checkpoints.py"

    if not path.exists():
        return

    text = path.read_text()

    new = re.sub(r"^s\[3\]\s*$\n?", "", text, flags=re.MULTILINE)

    if new != text:
        path.write_text(new)
        print("FIXED:", path.name, "(removed stray s[3])")
    else:
        print("OK:", path.name)


def patch_alias_installer():
    path = ROOT / "tools/genesis/genesis_8/install_safe_command_aliases.py"

    if not path.exists():
        return

    text = path.read_text()

    if "len(SAFE_COMMAND_ALIASES)" in text:
        replacement = (
            "len(SAFE_COMMAND_ALIASES)"
            if "SAFE_COMMAND_ALIASES =" in text
            else "len(alias_module.splitlines())"
        )

        new = text.replace(
            "len(SAFE_COMMAND_ALIASES)",
            replacement,
        )

        if new != text:
            path.write_text(new)
            print("PATCHED:", path.name)

    else:
        print("OK:", path.name)


def patch_backup():
    path = (
        ROOT
        / "reports/genesis_8_command_dispatch/"
        / "prediction_adapter_backup_20260710_050230/core.py"
    )

    if not path.exists():
        return

    text = path.read_text()

    if "session.to_dict()" not in text:
        print("OK:", path.name)
        return

    occurrences = text.count("session.to_dict()")

    if occurrences != 2:
        print(
            "MANUAL REVIEW:",
            path,
            f"({occurrences} occurrences)",
        )
        return

    print("NOTICE:", path.name, "contains archived undefined session reference.")
    print("Recommend manual inspection rather than blind replacement.")


def main():
    print("=" * 60)
    print("Genesis 11 F821 Repair")
    print("=" * 60)

    patch_streamlit()
    patch_validation()
    patch_alias_installer()
    patch_backup()

    print("=" * 60)
    print("Finished")
    print("=" * 60)


if __name__ == "__main__":
    main()
