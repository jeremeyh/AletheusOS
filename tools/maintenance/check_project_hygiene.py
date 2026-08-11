import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(".")
failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"✓ {name}")
    else:
        print(f"✗ {name} {detail}")
        failures.append(name)


print("=" * 70)
print("AletheusOS Project Hygiene")
print("=" * 70)

check("No patch scripts in root", not list(ROOT.glob("patch_v*.py")))
check("No verify scripts in root", not list(ROOT.glob("verify_v*.py")))
check("No setup scripts in root", not list(ROOT.glob("setup_v*.py")))
check("No fix scripts in root", not list(ROOT.glob("fix_*.py")))
check("No debug scripts in root", not list(ROOT.glob("debug_*.py")))

required_dirs = [
    "tools/patches/v2",
    "tools/patches/v3",
    "tools/patches/v3.7",
    "tools/patches/v3.9",
    "tools/patches/v4.0",
    "tools/patches/v4.1",
    "tools/patches/v4.2",
    "tools/patches/v4.3",
    "tools/patches/current",
    "tools/patches/archived/legacy",
    "tools/patches/archived/emergency",
    "tools/maintenance",
    "tools/verification",
    "tools/migration",
    "tools/generators",
    "tools/experiments",
    "docs/ARCHITECTURE",
    "docs/GENESIS",
    "RELEASE_NOTES",
]

for directory in required_dirs:
    check(f"Directory exists: {directory}", Path(directory).exists())

required_files = [
    "VERSION",
    "CHANGELOG.md",
    "docs/CONSTITUTION.md",
    "docs/ENGINEERING_GUIDE.md",
]

for file in required_files:
    path = Path(file)
    check(
        f"File exists: {file}",
        path.exists() and path.stat().st_size > 0,
        f"(exists={path.exists()}, size={path.stat().st_size if path.exists() else 0})",
    )

compile_result = subprocess.run(
    [sys.executable, "-m", "py_compile", "aletheus/runtime/core.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
check("Runtime core compiles", compile_result.returncode == 0)

version_file = Path("VERSION").read_text().strip() if Path("VERSION").exists() else ""
core_text = Path("aletheus/runtime/core.py").read_text()
match = re.search(r'self\.version\s*=\s*"([^"]+)"', core_text)
runtime_version = match.group(1) if match else ""

check(
    "VERSION matches runtime version",
    bool(version_file and runtime_version and version_file == runtime_version),
    f"(VERSION={version_file}, runtime={runtime_version})",
)

command_matches = re.findall(
    r'self\.commands\.register\("([^"]+)"',
    core_text,
)
duplicates = sorted({cmd for cmd in command_matches if command_matches.count(cmd) > 1})
check("No duplicate command registrations", not duplicates, str(duplicates))

patch_names = {}
duplicate_patch_names = []

for patch in Path("tools/patches").rglob("patch_*.py"):
    if patch.name in patch_names:
        duplicate_patch_names.append(patch.name)
    patch_names[patch.name] = patch

check(
    "No duplicate patch filenames",
    not duplicate_patch_names,
    str(duplicate_patch_names),
)

if failures:
    print("\nFAILED:")
    for failure in failures:
        print(f"- {failure}")
    print("\nProject hygiene status: FAILED")
    raise SystemExit(1)

print("\nProject hygiene status: HEALTHY")
