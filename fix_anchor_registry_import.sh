#!/bin/bash

set -e

echo "==============================================="
echo " Fixing AletheusOS Anchor Registry Import"
echo "==============================================="


CORE="aletheus/runtime/core.py"


cp "$CORE" "${CORE}.before_anchor_fix"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


import_block = """
from aletheus.runtime.anchors.registry import AnchorRegistry
"""


# Insert before class definition
marker = "class AletheusRuntime:"


if "from aletheus.runtime.anchors.registry import AnchorRegistry" not in text:

    text = text.replace(
        marker,
        import_block + "\n\n" + marker
    )

    print("Added AnchorRegistry import")

else:

    print("AnchorRegistry import already exists")


path.write_text(text)

PY


echo ""
echo "Checking import..."

python3 - <<'PY'
import ast

path="aletheus/runtime/core.py"

with open(path) as f:
    ast.parse(f.read())

print("core.py syntax OK")
PY


echo ""
echo "Testing AnchorRegistry availability..."

python3 - <<'PY'

import aletheus.runtime.core as core

print("AnchorRegistry:",
      core.AnchorRegistry)

PY


echo ""
echo "==============================================="
echo " Anchor Registry Repair Complete"
echo "==============================================="

