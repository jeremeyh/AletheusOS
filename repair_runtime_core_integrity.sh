#!/bin/bash

set -e

echo "================================================"
echo " AletheusOS Runtime Core Integrity Repair"
echo " Composition Root Recovery"
echo "================================================"


CORE="aletheus/runtime/core.py"


if [ ! -f "$CORE" ]; then
    echo "ERROR: core.py not found"
    exit 1
fi


echo "[1/5] Creating backup..."

cp "$CORE" "${CORE}.repair_backup"


echo "[2/5] Repairing imports..."

python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


imports = """

# =====================================================
# Runtime Core Dependency Imports
# =====================================================

from aletheus.runtime.anchors.registry import AnchorRegistry

from aletheus.runtime.anchors.lifecycle import (
    AnchorLifecycleController
)

from aletheus.runtime.anchors.dependency_graph import (
    AnchorDependencyGraph
)

from aletheus.runtime.anchors.governance import (
    AnchorGovernanceAnalyzer
)


from aletheus.runtime.circuits import (
    IntelligenceAnchorCircuit,
    MemoryAnchorCircuit,
    KnowledgeAnchorCircuit,
    ApplicationAnchorCircuit
)

"""


marker = "class AletheusRuntime:"


if imports not in text:

    text = text.replace(
        marker,
        imports + "\n\n" + marker
    )

    print("Added runtime dependency imports")

else:

    print("Imports already present")


path.write_text(text)

PY



echo "[3/5] Restoring runtime compatibility exports..."


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


footer = """

# =====================================================
# Runtime Compatibility Exports
# =====================================================


class RuntimeContext:

    def __init__(self):

        self.results = {}


    def add_result(
        self,
        key,
        value
    ):

        self.results[key] = value



runtime_core = AletheusRuntime()

"""


if "runtime_core = AletheusRuntime()" not in text:

    text += footer

    print("Added runtime_core export")

else:

    print("runtime_core already exists")


path.write_text(text)

PY



echo "[4/5] Compile validation..."

python3 -m compileall aletheus/runtime/core.py



echo "[5/5] Runtime import validation..."


python3 - <<'PY'

from aletheus.runtime.core import (
    AletheusRuntime,
    RuntimeContext,
    runtime_core
)

print("Runtime class:", AletheusRuntime)

print("Runtime context:", RuntimeContext())

print("Runtime core:", runtime_core)


PY



echo ""
echo "================================================"
echo " RUNTIME CORE REPAIR COMPLETE"
echo "================================================"

