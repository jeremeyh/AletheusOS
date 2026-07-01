from pathlib import Path
import sys

CORE = Path("aletheus/runtime/core.py")

if not CORE.exists():
    sys.exit("runtime/core.py not found.")

text = CORE.read_text()
changed = False

# --------------------------------------------------
# Import PrincipleXValidator
# --------------------------------------------------

import_line = "from aletheus.runtime.governance import GovernanceEngine, PrincipleXValidator"

old_import = "from aletheus.runtime.governance import GovernanceEngine"

if old_import in text and import_line not in text:
    text = text.replace(old_import, import_line, 1)
    changed = True

# --------------------------------------------------
# Instantiate validator
# --------------------------------------------------

old = "        self.governance = GovernanceEngine(self)"

new = """        self.governance = GovernanceEngine(self)
        self.principle_x = PrincipleXValidator(self)"""

if old in text and "self.principle_x" not in text:
    text = text.replace(old, new, 1)
    changed = True

CORE.write_text(text)

if changed:
    print("✔ Principle X integrated.")
else:
    print("✔ Already integrated.")
