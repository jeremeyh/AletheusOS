#!/usr/bin/env python3

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCTOR = ROOT / "tools" / "repository" / "doctor.py"

if not DOCTOR.exists():
    raise SystemExit(f"Unable to locate {DOCTOR}")

backup = DOCTOR.with_suffix(".py.bak")
shutil.copy2(DOCTOR, backup)

text = DOCTOR.read_text(encoding="utf-8")

#
# 1. Update namespace_findings() signature
#
old = """def namespace_findings(root: Path) -> list[Finding]:"""

new = """def namespace_findings(
    root: Path,
    policy: dict[str, Any],
) -> list[Finding]:"""

if old in text:
    text = text.replace(old, new, 1)
else:
    print("Signature already updated.")

#
# 2. Update run_doctor() call site
#
old = """findings.extend(namespace_findings(REPOSITORY_ROOT))"""

new = """findings.extend(namespace_findings(REPOSITORY_ROOT, policy))"""

if old in text:
    text = text.replace(old, new, 1)
else:
    print("Call site already updated.")

DOCTOR.write_text(text, encoding="utf-8")

print("✓ Updated namespace_findings() signature")
print("✓ Updated run_doctor() call")
print(f"✓ Backup: {backup}")
