#!/bin/bash

set -e


echo "================================================"
echo " AletheusOS Registry Federation Wiring v2"
echo " Runtime Repair + Intelligence Integration"
echo "================================================"


ROOT="aletheus"


# =================================================
# RUNTIME IMPORT REPAIR
# =================================================

echo "[1/5] Checking runtime/core.py integrity..."


CORE_FILE="$ROOT/runtime/core.py"


if [ -f "$CORE_FILE" ]; then

python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

if path.exists():

    text = path.read_text()

    broken = (
        "from aletheus.runtime.services import ServiceRegistry"
        "from aletheus.runtime.integrity import RuntimeInvariantEngine, RuntimeBootValidator"
    )

    fixed = (
        "from aletheus.runtime.services import ServiceRegistry\n"
        "from aletheus.runtime.integrity import RuntimeInvariantEngine, RuntimeBootValidator"
    )


    if broken in text:

        text = text.replace(
            broken,
            fixed
        )

        path.write_text(text)

        print(
            "Fixed concatenated runtime imports"
        )

    else:

        print(
            "No runtime import corruption detected"
        )

PY

else

echo "WARNING: runtime/core.py not found"

fi



# =================================================
# COMPILE VALIDATION
# =================================================

echo "[2/5] Validating runtime..."

python3 -m compileall "$ROOT/runtime"



# =================================================
# REGISTRY FEDERATION VALIDATION
# =================================================

echo "[3/5] Validating Registry Federation..."


python3 -m compileall \
"$ROOT/registry_federation"



# =================================================
# RUN FEDERATION
# =================================================

echo "[4/5] Running Registry Federation..."


python3 -m aletheus.registry_federation.federator



# =================================================
# FINAL PLATFORM CHECK
# =================================================

echo "[5/5] Running AletheusOS validation..."


python3 -m compileall "$ROOT"



echo ""
echo "================================================"
echo " REGISTRY FEDERATION v2 COMPLETE"
echo "================================================"

echo ""

if [ -f "$ROOT/registry_federation/wiring_report.json" ]; then

echo "Wiring Report Generated:"
echo "$ROOT/registry_federation/wiring_report.json"

else

echo "WARNING: Wiring report not generated"

fi


echo ""
echo "AletheusOS Registry Intelligence Layer ACTIVE"

