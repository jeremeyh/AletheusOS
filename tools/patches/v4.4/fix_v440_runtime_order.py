from pathlib import Path
import re
import sys

CORE = Path("aletheus/runtime/core.py")

if not CORE.exists():
    sys.exit("runtime/core.py not found.")

text = CORE.read_text()

# -------------------------------------------------------
# Fix imports
# -------------------------------------------------------

text = re.sub(
    r"from aletheus\.runtime\.registries import EngineRegistry, ServiceRegistry",
    "from aletheus.runtime.registries import EngineRegistry",
    text,
)

text = re.sub(
    r"from aletheus\.runtime\.services import ServiceRegistry, PrincipleXValidator",
    "from aletheus.runtime.services import ServiceRegistry",
    text,
)

# Remove duplicate Governance import
text = re.sub(
    r"from aletheus\.runtime\.governance import GovernanceEngine\s*\n",
    "",
    text,
    count=1,
)

gov_import = """from aletheus.runtime.governance import (
    GovernanceEngine,
    PrincipleXValidator,
)"""

if gov_import not in text:

    text = text.replace(
        "from aletheus.runtime.services import ServiceRegistry",
        gov_import + "\nfrom aletheus.runtime.services import ServiceRegistry",
        1,
    )

# -------------------------------------------------------
# Remove ALL previous service registrations
# -------------------------------------------------------

text = re.sub(
    r'(?:^[ \t]*self\.services\.register\([^\n]+\)\n?)+',
    '',
    text,
    flags=re.MULTILINE,
)

# -------------------------------------------------------
# Ensure ServiceRegistry exists
# -------------------------------------------------------

if "self.services = ServiceRegistry()" not in text:

    anchor = "self.governance = GovernanceEngine(self)"

    if anchor not in text:
        sys.exit("Governance initialization not found.")

    text = text.replace(
        anchor,
        "self.services = ServiceRegistry()\n        " + anchor,
        1,
    )

# -------------------------------------------------------
# Reinsert registrations AFTER boot validator
# -------------------------------------------------------

registration_block = """

        # --------------------------------------------------
        # Runtime Service Registry
        # --------------------------------------------------

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

anchor = "self.boot_validator = RuntimeBootValidator(self)"

if anchor not in text:
    sys.exit("Boot validator initialization not found.")

text = text.replace(
    anchor,
    anchor + registration_block,
    1,
)

# -------------------------------------------------------
# Clean blank lines
# -------------------------------------------------------

text = re.sub(r"\n{4,}", "\n\n\n", text)

CORE.write_text(text)

print("✔ Runtime import and initialization order repaired.")
