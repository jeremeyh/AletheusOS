from pathlib import Path

FILE = Path("tests/span/test_genesis14.py")

if not FILE.exists():
    raise SystemExit(f"Missing {FILE}")

text = FILE.read_text(encoding="utf-8")

replacements = {
    "assert not report.errors": "assert report.ok, report.to_dict()",
    "assert len(report.errors) == 0": "assert report.error_count == 0, report.to_dict()",
    "assert report.errors == []": "assert report.error_count == 0, report.to_dict()",
    "if report.errors:": "if not report.ok:",
    "len(report.errors)": "report.error_count",
}

count = 0
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new)
        count += 1

FILE.write_text(text, encoding="utf-8")

print(f"✓ Updated {FILE}")
print(f"✓ Applied {count} compatibility replacement(s)")
