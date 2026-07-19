from pathlib import Path
import re

core = Path("aletheus/runtime/core.py").read_text()

print("=" * 60)
print("AletheusOS Runtime Integrity Audit")
print("=" * 60)

# ----------------------------------------------------
# Duplicate command registrations
# ----------------------------------------------------
commands = re.findall(r'self\.commands\.register\("([^"]+)"', core)

duplicates = sorted(
    {c for c in commands if commands.count(c) > 1}
)

print("\nDuplicate Commands")
print("------------------")

if duplicates:
    for c in duplicates:
        print(c)
else:
    print("None")

# ----------------------------------------------------
# Duplicate services
# ----------------------------------------------------
services = re.findall(r'self\.services\.register\("([^"]+)"', core)

duplicates = sorted(
    {s for s in services if services.count(s) > 1}
)

print("\nDuplicate Services")
print("------------------")

if duplicates:
    for s in duplicates:
        print(s)
else:
    print("None")

# ----------------------------------------------------
# Legacy distributed references
# ----------------------------------------------------
legacy = re.findall(r'distributed_v3|distributed_core', core)

print("\nLegacy Distributed References")
print("-----------------------------")

print(len(legacy))

# ----------------------------------------------------
# Runtime version
# ----------------------------------------------------
m = re.search(r'self\.version = "([^"]+)"', core)

print("\nRuntime Version")
print("----------------")

print(m.group(1) if m else "Unknown")

print("\nAudit complete.")
