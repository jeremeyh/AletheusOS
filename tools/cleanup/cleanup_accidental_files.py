import shutil
from pathlib import Path

ROOT = Path(".").resolve()

targets = [
    Path("engine/_ _init_ _ .py"),
    Path("engine/hawk_a_eye/_ _init_ _ .py"),
    Path("engine/thorx/_ _init_ _ .py"),
    Path("..."),
]

print("=========================================")
print("AletheusOS Cleanup: Accidental Files")
print("=========================================")

for target in targets:
    path = ROOT / target

    if not path.exists():
        print(f"✓ Not found, skipping: {target}")
        continue

    if path.is_dir():
        shutil.rmtree(path)
        print(f"✓ Removed directory: {target}")
    else:
        path.unlink()
        print(f"✓ Removed file: {target}")

print()
print("Verifying malformed init files...")
bad = list(ROOT.rglob("_ _init_ _ .py"))

if bad:
    print("✗ Remaining malformed init files:")
    for item in bad:
        print(f"  {item.relative_to(ROOT)}")
    raise SystemExit(1)

print("✓ No malformed init files remain.")
print("✓ Cleanup complete.")
