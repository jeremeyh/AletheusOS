#!/bin/bash

set -e

echo "================================================"
echo " Fix Anchor Governance Dependency Injection"
echo "================================================"

FILE="aletheus/runtime/core.py"

cp "$FILE" "${FILE}.before_governance_di_fix"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


old = "AnchorGovernanceCouncil(self)"


new = """AnchorGovernanceCouncil(
        self.prediction,
        self.intelligence
    )"""


if old in text:

    text = text.replace(
        old,
        new
    )

    print("Governance dependency injection repaired")

else:

    print("Target constructor call not found")


path.write_text(text)

PY


python3 -m compileall aletheus/runtime/core.py


python3 - <<'PY'

from aletheus.runtime.core import runtime_core

print("SUCCESS")
print(runtime_core)

PY


echo "================================================"
echo " Governance Wiring Complete"
echo "================================================"

