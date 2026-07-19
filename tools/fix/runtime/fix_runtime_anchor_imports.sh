#!/bin/bash

set -e

echo "================================================"
echo " Restoring AletheusOS Runtime Anchor Imports"
echo "================================================"


FILE="aletheus/runtime/core.py"


cp "$FILE" "${FILE}.before_anchor_import_restore"



python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


imports = """

# =====================================================
# Runtime Anchor Framework Imports
# =====================================================

from aletheus.runtime.anchors import (
    AnchorRegistry,
    AnchorLifecycleController,
    AnchorDependencyGraph,
    AnchorGovernanceAnalyzer,
    IntelligenceAnchorCircuit,
    MemoryAnchorCircuit,
    KnowledgeAnchorCircuit,
    ApplicationAnchorCircuit,
)

"""


marker = "class AletheusRuntime:"


if "AnchorLifecycleController" not in text.split(marker)[0]:

    text = text.replace(
        marker,
        imports + "\n" + marker
    )

    print("Restored runtime anchor imports")

else:

    print("Anchor imports already present")


path.write_text(text)

PY


python3 -m compileall aletheus/runtime/core.py


python3 - <<'PY'

from aletheus.runtime.core import runtime_core

print("Runtime core loaded:")
print(runtime_core)

PY


echo "================================================"
echo " Runtime Anchor Import Restoration Complete"
echo "================================================"

