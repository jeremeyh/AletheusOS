from pathlib import Path
import subprocess
import sys

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

check("VERSION exists", Path("VERSION").exists())
check("CHANGELOG exists", Path("CHANGELOG.md").exists())
check("Release notes folder exists", Path("RELEASE_NOTES").exists())
check("Constitution exists", Path("docs/CONSTITUTION.md").exists())
check("Engineering guide exists", Path("docs/ENGINEERING_GUIDE.md").exists())

compile_result = subprocess.run(
    [sys.executable, "-m", "py_compile", "aletheus/runtime/core.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

check("Runtime compiles", compile_result.returncode == 0)

if failures:
    print("\nFAILED:")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("\nProject hygiene status: HEALTHY")
