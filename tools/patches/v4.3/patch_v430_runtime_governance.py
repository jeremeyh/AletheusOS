from pathlib import Path
import sys

CORE = Path("aletheus/runtime/core.py")

if not CORE.exists():
    sys.exit("runtime/core.py not found")

text = CORE.read_text()
changed = False

# -------------------------------------------------
# Import GovernanceEngine
# -------------------------------------------------

import_line = "from aletheus.runtime.governance import GovernanceEngine"

if import_line not in text:

    anchor = "from aletheus.runtime.integrity import RuntimeDoctor"

    if anchor not in text:
        sys.exit("Could not locate RuntimeDoctor import.")

    text = text.replace(
        anchor,
        anchor + "\n" + import_line,
        1,
    )

    changed = True

# -------------------------------------------------
# Instantiate Governance Engine
# -------------------------------------------------

assignment = "        self.governance = GovernanceEngine(self)"

if assignment not in text:

    anchor = "        self.runtime_doctor = RuntimeDoctor(self)"

    if anchor not in text:
        sys.exit("Could not locate RuntimeDoctor initialization.")

    text = text.replace(
        anchor,
        anchor + "\n" + assignment,
        1,
    )

    changed = True

if changed:
    CORE.write_text(text)
    print("✔ Governance Engine integrated.")
else:
    print("✔ Governance Engine already integrated.")
