from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

changed = False

# -------------------------------------------------
# Import
# -------------------------------------------------

if "from aletheus.high_availability_v3 import high_availability_core" not in text:
    if "from aletheus.telemetry_v3 import telemetry_core" in text:
        text = text.replace(
            "from aletheus.telemetry_v3 import telemetry_core",
            "from aletheus.telemetry_v3 import telemetry_core\nfrom aletheus.high_availability_v3 import high_availability_core",
            1,
        )
        changed = True
    else:
        print("ERROR: telemetry import not found")

# -------------------------------------------------
# Runtime initialization
# -------------------------------------------------

if "self.high_availability_v3 = high_availability_core" not in text:
    if "self.telemetry_v3 = telemetry_core" in text:
        text = text.replace(
            "self.telemetry_v3 = telemetry_core",
            "self.telemetry_v3 = telemetry_core\n        self.high_availability_v3 = high_availability_core",
            1,
        )
        changed = True
    else:
        print("ERROR: telemetry initialization not found")

# -------------------------------------------------
# Version
# -------------------------------------------------

text = text.replace(
    'self.version = "3.5.0"',
    'self.version = "3.6.0"',
)

# -------------------------------------------------
# Command registration
# -------------------------------------------------

if 'self.commands.register("ha.bootstrap"' not in text:
    anchor = (
        'self.commands.register("telemetry.statistics", self._cmd_telemetry_statistics)'
    )

    if anchor in text:
        replacement = (
            anchor
            + """

        # v3.6 High Availability

        self.commands.register("ha.bootstrap", self._cmd_ha_bootstrap)
        self.commands.register("ha.join", self._cmd_ha_join)
        self.commands.register("ha.leave", self._cmd_ha_leave)
        self.commands.register("ha.promote", self._cmd_ha_promote)
        self.commands.register("ha.demote", self._cmd_ha_demote)
        self.commands.register("ha.failover", self._cmd_ha_failover)
        self.commands.register("ha.recover", self._cmd_ha_recover)
        self.commands.register("ha.replicate", self._cmd_ha_replicate)
        self.commands.register("ha.status", self._cmd_ha_status)
        self.commands.register("ha.statistics", self._cmd_ha_statistics)
"""
        )

        text = text.replace(anchor, replacement, 1)
        changed = True
    else:
        print("ERROR: telemetry command registration not found")

if changed:
    core.write_text(text)
    print("✔ Runtime repaired.")
else:
    print("Nothing changed.")
