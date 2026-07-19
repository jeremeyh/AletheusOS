#!/bin/bash

set -e

echo "================================================"
echo " Fix IntelligenceAnchorCircuit Runtime Init"
echo "================================================"

FILE="aletheus/runtime/anchors/intelligence.py"

cp "$FILE" "${FILE}.before_runtime_init_fix"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/anchors/intelligence.py")

text = path.read_text()

text = text.replace(
    "super().__init__()",
    "super().__init__(runtime)"
)

path.write_text(text)

print("Fixed RuntimeAnchorCircuit initialization")

PY


python3 -m compileall "$FILE"

echo "================================================"
echo " Complete"
echo "================================================"

