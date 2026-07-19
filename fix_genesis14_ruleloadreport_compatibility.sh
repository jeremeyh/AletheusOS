\
#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

echo "Patching Genesis 14 RuleLoadReport compatibility..."

python <<'PY'
from pathlib import Path
import re

# Patch api.py
api = Path("aletheus/span/api.py")
text = api.read_text()

text = re.sub(
    r'report = RuleLoader\(registry\)\.load_all\(strict=True\)\s*'
    r'if not report\.ok:\s*'
    r'raise RuntimeError\(\s*f"SPAN rule loading failed: \{report\.errors\}"\s*\)',
    'report = RuleLoader(registry).load_all(strict=True)',
    text,
    flags=re.S,
)

text = text.replace(
    'raise RuntimeError(f"SPAN rule loading failed: {report.errors}")',
    'raise RuntimeError(f"SPAN rule loading failed: {report.summary()}")'
)

text = text.replace("if report.errors:", "if not report.ok:")

api.write_text(text)

# Patch validate.sh
val = Path("Genesis14_SPAN_Constitutional_Intelligence/validate.sh")
if val.exists():
    t = val.read_text()
    t = t.replace("assert not load_report.errors", "assert load_report.ok")
    val.write_text(t)

print("Compatibility patch applied.")
PY

echo
echo "Re-running validation..."

./Genesis14_SPAN_Constitutional_Intelligence/validate.sh
