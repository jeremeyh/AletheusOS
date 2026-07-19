#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

FILE="aletheus/span/bootstrap.py"

python - <<'PY'
from pathlib import Path

path = Path("aletheus/span/bootstrap.py")
text = path.read_text()

if "def run(self, project_root" not in text:
    marker = "    def shutdown(self) -> None:\n"
    shim = (
        "    def run(self, project_root: str | None = None) -> \"SPANBootstrap\":\n"
        "        \"\"\"Legacy compatibility entry point.\"\"\"\n"
        "        self.initialize()\n"
        "        return self\n\n"
        "    @property\n"
        "    def ready(self) -> bool:\n"
        "        return self.initialized\n\n"
        "    def status(self):\n"
        "        return self.report\n\n"
    )
    if marker not in text:
        raise RuntimeError("shutdown() not found")
    text = text.replace(marker, shim + marker)

path.write_text(text)
print("Compatibility shim installed.")
PY

python -m py_compile "$FILE"

python - <<'PY'
from aletheus.span.bootstrap import SPANBootstrap

b = SPANBootstrap()
assert b.run('.') is b
assert b.ready
assert b.status() is b.report
print("run(): OK")
print("ready: OK")
print("status(): OK")
PY

echo
echo "Genesis 13.5.1 compatibility repair completed."
