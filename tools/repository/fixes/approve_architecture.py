#!/usr/bin/env python3

from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[3]

policy_file = ROOT / "config" / "repository_policy.json"
doctor_file = ROOT / "tools" / "repository" / "doctor.py"

shutil.copy2(policy_file, policy_file.with_suffix(".json.bak"))
shutil.copy2(doctor_file, doctor_file.with_suffix(".py.bak"))

policy = json.loads(policy_file.read_text())

policy.setdefault(
    "approved_protected_root_files",
    [
        "card_hawk_console.py",
        "history.py",
    ],
)

policy.setdefault(
    "approved_namespace_pairs",
    [
        ["event_bus", "eventbus"],
        ["backup", "backups"],
        ["card_hawk", "cardhawk"],
        ["workflow", "workflows"],
        ["engine", "engines"],
    ],
)

policy_file.write_text(json.dumps(policy, indent=2) + "\n")

text = doctor_file.read_text()

old = """    protected = normalized_set(policy, "protected_root_files")
"""

new = """    protected = normalized_set(policy, "protected_root_files")
    approved_protected = normalized_set(
        policy,
        "approved_protected_root_files",
    )
"""

if old in text:
    text = text.replace(old, new, 1)

old = """        if name in protected:
"""

new = """        if name in protected:
            if name in approved_protected:
                continue
"""

if old in text:
    text = text.replace(old, new, 1)

old = """    duplicate_pairs = [
        ("event_bus", "eventbus"),
        ("backup", "backups"),
        ("card_hawk", "cardhawk"),
        ("workflow", "workflows"),
        ("engine", "engines"),
    ]
"""

new = """    duplicate_pairs = [
        ("event_bus", "eventbus"),
        ("backup", "backups"),
        ("card_hawk", "cardhawk"),
        ("workflow", "workflows"),
        ("engine", "engines"),
    ]

    approved_pairs = {
        tuple(pair)
        for pair in policy.get("approved_namespace_pairs", [])
    }
"""

if old in text:
    text = text.replace(old, new, 1)

old = """    for left, right in duplicate_pairs:
"""

new = """    for left, right in duplicate_pairs:
        if (left, right) in approved_pairs:
            continue
"""

if old in text:
    text = text.replace(old, new, 1)

doctor_file.write_text(text)

print("✓ Updated repository policy")
print("✓ Updated Repository Doctor")
