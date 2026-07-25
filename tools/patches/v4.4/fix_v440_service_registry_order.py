import re
import sys
from pathlib import Path

CORE = Path("aletheus/runtime/core.py")

if not CORE.exists():
    sys.exit("runtime/core.py not found.")

text = CORE.read_text()

service_lines = [
    '        self.services.register("commands", self.commands)',
    '        self.services.register("events", self.events)',
    '        self.services.register("metrics", self.metrics)',
    '        self.services.register("compatibility", self.compat)',
    '        self.services.register("kernel", self.kernel)',
    '        self.services.register("governance", self.governance)',
    '        self.services.register("doctor", self.runtime_doctor)',
    '        self.services.register("boot_validator", self.boot_validator)',
    '        self.services.register("invariants", self.runtime_invariants)',
]

service_block = "\n".join(service_lines)

# Remove existing service registration lines wherever they were inserted.
for line in service_lines:
    text = text.replace(line + "\n", "")
    text = text.replace(line, "")

# Ensure ServiceRegistry import exists.
if "from aletheus.runtime.services import ServiceRegistry" not in text:
    anchor = "from aletheus.runtime.governance import GovernanceEngine"
    if anchor not in text:
        anchor = "from aletheus.runtime.governance import GovernanceEngine, PrincipleXValidator"

    if anchor not in text:
        sys.exit("Could not locate governance import anchor.")

    text = text.replace(
        anchor,
        anchor + "\nfrom aletheus.runtime.services import ServiceRegistry",
        1,
    )

# Ensure registry exists before governance/service registration.
if "self.services = ServiceRegistry()" not in text:
    anchor = "        self.governance = GovernanceEngine(self)"
    if anchor not in text:
        sys.exit("Could not locate governance initialization anchor.")

    text = text.replace(
        anchor,
        "        self.services = ServiceRegistry()\n" + anchor,
        1,
    )

# Insert service registrations after all required services exist.
anchors = [
    "        self.boot_validator = RuntimeBootValidator(self)",
    "        self.runtime_invariants = RuntimeInvariantEngine(self)",
    "        self.runtime_doctor = RuntimeDoctor(self)",
]

insert_anchor = None
for anchor in anchors:
    if anchor in text:
        insert_anchor = anchor

if insert_anchor is None:
    sys.exit("Could not locate integrity initialization anchor.")

if 'self.services.register("commands", self.commands)' not in text:
    text = text.replace(
        insert_anchor,
        insert_anchor + "\n\n" + service_block,
        1,
    )

# Normalize accidental blank line runs.
text = re.sub(r"\n{4,}", "\n\n\n", text)

CORE.write_text(text)

print("✔ Service Registry order repaired.")
