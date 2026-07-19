#!/bin/bash

set -e

echo "================================================"
echo " AletheusOS Runtime Diagnostics Order Repair"
echo "================================================"

FILE="aletheus/runtime/core.py"

cp "$FILE" "${FILE}.before_diagnostics_order_fix"


python3 - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


init = "        self.diagnostics = RuntimeDiagnostics(self)"


bootstrap = "        self._bootstrap_runtime_registry()"


if init in text and bootstrap in text:

    init_pos = text.find(init)
    boot_pos = text.find(bootstrap)

    if init_pos > boot_pos:

        print("Moving diagnostics initialization before registry bootstrap")

        text = text.replace(
            init,
            ""
        )

        text = text.replace(
            bootstrap,
            init + "\n\n" + bootstrap
        )

    else:

        print("Diagnostics already initialized before bootstrap")

else:

    raise Exception(
        "Could not find required runtime statements"
    )


path.write_text(text)

PY


python3 -m compileall aletheus/runtime/core.py


python3 - <<'PY'

from aletheus.runtime.core import runtime_core

print("SUCCESS")
print(runtime_core)

PY


echo "================================================"
echo " Diagnostics Ordering Fixed"
echo "================================================"

