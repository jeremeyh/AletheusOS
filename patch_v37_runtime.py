from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

changed = False

# -------------------------------------------------
# Import
# -------------------------------------------------

if "from aletheus.security_v3 import security_core" not in text:

    anchor = "from aletheus.high_availability_v3 import high_availability_core"

    if anchor not in text:
        raise SystemExit("High Availability import anchor not found.")

    text = text.replace(
        anchor,
        anchor +
        "\nfrom aletheus.security_v3 import security_core",
        1,
    )

    changed = True

# -------------------------------------------------
# Runtime Initialization
# -------------------------------------------------

if "self.security_v3 = security_core" not in text:

    anchor = "self.high_availability_v3 = high_availability_core"

    if anchor not in text:
        raise SystemExit("HA initialization anchor not found.")

    text = text.replace(
        anchor,
        anchor +
        "\n        self.security_v3 = security_core",
        1,
    )

    changed = True

# -------------------------------------------------
# Runtime Version
# -------------------------------------------------

text = text.replace(
    'self.version = "3.6.0"',
    'self.version = "3.7.0"',
)

# -------------------------------------------------
# Commands
# -------------------------------------------------

if 'self.commands.register("security.bootstrap"' not in text:

    anchor = 'self.commands.register("ha.statistics", self._cmd_ha_statistics)'

    if anchor not in text:
        raise SystemExit("HA command anchor not found.")

    replacement = anchor + '''

        # --------------------------------------------------
        # v3.7 Security & Policy Engine
        # --------------------------------------------------

        self.commands.register("security.bootstrap", self._cmd_security_bootstrap)
        self.commands.register("security.authenticate", self._cmd_security_authenticate)
        self.commands.register("security.authorize", self._cmd_security_authorize)
        self.commands.register("security.policy", self._cmd_security_policy)
        self.commands.register("security.role.create", self._cmd_security_role_create)
        self.commands.register("security.role.assign", self._cmd_security_role_assign)
        self.commands.register("security.audit", self._cmd_security_audit)
        self.commands.register("security.statistics", self._cmd_security_statistics)
'''

    text = text.replace(anchor, replacement, 1)
    changed = True

if changed:
    core.write_text(text)
    print("✔ AletheusOS v3.7 runtime integrated.")
else:
    print("✔ Runtime already up to date.")
