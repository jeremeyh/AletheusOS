from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2] / "rust"

# Matches float literals beginning with a decimal point,
# but avoids touching existing values like 10.55 or member access.
PATTERN = re.compile(r'(?<![\w\d])\.(\d+)')

fixed_files = 0
fixed_literals = 0

for path in ROOT.rglob("*.rs"):
    text = path.read_text(encoding="utf-8")

    new_text, count = PATTERN.subn(r"0.\1", text)

    if count:
        path.write_text(new_text, encoding="utf-8")
        fixed_files += 1
        fixed_literals += count
        print(f"✓ {path.relative_to(ROOT)} ({count} fixes)")

print()
print("=" * 72)
print(f"Files fixed    : {fixed_files}")
print(f"Literals fixed : {fixed_literals}")
print("=" * 72)
