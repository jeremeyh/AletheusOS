import sys
from pathlib import Path

CORE = Path("aletheus/runtime/core.py")

if not CORE.exists():
    sys.exit("runtime/core.py not found.")

text = CORE.read_text()
changed = False

# --------------------------------------------------
# Import ServiceRegistry
# --------------------------------------------------

old_import = "from aletheus.runtime.governance import GovernanceEngine, PrincipleXValidator"
new_import = old_import + "\nfrom aletheus.runtime.services import ServiceRegistry"

if old_import in text and "ServiceRegistry" not in text:
    text = text.replace(old_import, new_import, 1)
    changed = True

# --------------------------------------------------
# Instantiate registry
# --------------------------------------------------

anchor = "        self.governance = GovernanceEngine(self)"

if anchor in text and "self.services = ServiceRegistry()" not in text:
    text = text.replace(
        anchor,
        anchor + "\n        self.services = ServiceRegistry()",
        1,
    )
    changed = True

# --------------------------------------------------
# Register services
# --------------------------------------------------

registration_anchor = "        self.boot()"

registration_block = """
        self.services.register("commands", self.commands)
        self.services.register("events", self.events)
        self.services.register("metrics", self.metrics)
        self.services.register("compatibility", self.compat)
        self.services.register("kernel", self.kernel)
        self.services.register("governance", self.governance)
        self.services.register("doctor", self.runtime_doctor)
        self.services.register("boot_validator", self.boot_validator)
        self.services.register("invariants", self.runtime_invariants)
"""

if registration_anchor in text and 'self.services.register("commands"' not in text:
    text = text.replace(
        registration_anchor,
        registration_block + "\n" + registration_anchor,
        1,
    )
    changed = True

CORE.write_text(text)

print("✔ v4.4 Service Registry integrated." if changed else "✔ Already integrated.")
