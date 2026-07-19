#!/usr/bin/env bash
set -Eeuo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${1:-$(pwd)}"
cd "$PROJECT_ROOT"

required=(
  "aletheus/span/finding.py"
  "aletheus/span/rule_engine.py"
  "aletheus/span/rule_registry.py"
  "aletheus/span/rule_loader.py"
  "aletheus/span/bootstrap.py"
  "aletheus/span/integration.py"
)
for file in "${required[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "ERROR: Missing Genesis 13 prerequisite: $file"
    echo "Run this installer from the AletheusOS project root after Genesis 13.5.2."
    exit 1
  fi
done

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP="reports/span/backups/genesis14_${STAMP}"
mkdir -p "$BACKUP"

targets=(
  "aletheus/span/api.py"
  "aletheus/span/constitutional_context.py"
  "aletheus/span/profiles.py"
  "aletheus/span/reporter.py"
  "aletheus/span/rules"
  "aletheus/span/profiles"
  "aletheus/span/docs"
  "tests/span/test_genesis14.py"
  "aletheus/span/__init__.py"
)
for target in "${targets[@]}"; do
  if [[ -e "$target" ]]; then
    mkdir -p "$BACKUP/$(dirname "$target")"
    cp -R "$target" "$BACKUP/$target"
  fi
done

mkdir -p aletheus/span tests/span
cp -R "$PACKAGE_DIR/package/aletheus/span/." aletheus/span/
cp "$PACKAGE_DIR/tests/test_genesis14.py" tests/span/test_genesis14.py

INIT="aletheus/span/__init__.py"
touch "$INIT"
python - "$INIT" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
start = "# BEGIN GENESIS 14 PUBLIC API"
end = "# END GENESIS 14 PUBLIC API"
block = """# BEGIN GENESIS 14 PUBLIC API
from .api import SPAN
from .profiles import RuleProfile, load_profile
from .reporter import SPANReport
# END GENESIS 14 PUBLIC API
"""
if start in text and end in text:
    before = text.split(start, 1)[0]
    after = text.split(end, 1)[1]
    text = before.rstrip() + "\n\n" + block + after.lstrip("\n")
else:
    text = text.rstrip() + "\n\n" + block
path.write_text(text)
PY

printf '%s\n' "$BACKUP" > reports/span/backups/genesis14_latest.txt

echo
echo "Genesis 14 files installed."
"$PACKAGE_DIR/validate.sh" "$PROJECT_ROOT"

echo
echo "======================================================"
echo "Genesis 14.0 SPAN Constitutional Intelligence"
echo "Installed and validated successfully."
echo "======================================================"
echo "Backup: $BACKUP"
echo
echo "Run an analysis:"
echo "python - <<'PY'"
echo "from aletheus.span import SPAN"
echo "report = SPAN('aletheus/span/profiles/constitutional.yaml').analyze('.')"
echo "print(report.to_markdown())"
echo "PY"
