from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# --------------------------------------------------
# Import
# --------------------------------------------------

if "from aletheus.high_availability_v3 import high_availability_core" not in text:

    anchor = "from aletheus.telemetry_v3 import telemetry_core\n"

    if anchor not in text:
        raise SystemExit("Telemetry import anchor not found.")

    text = text.replace(
        anchor,
        anchor +
        "from aletheus.high_availability_v3 import high_availability_core\n",
        1,
    )

# --------------------------------------------------
# Runtime initialization
# --------------------------------------------------

if "self.high_availability_v3 = high_availability_core" not in text:

    anchor = "self.telemetry_v3 = telemetry_core"

    if anchor not in text:
        raise SystemExit("Telemetry runtime anchor not found.")

    text = text.replace(
        anchor,
        anchor +
        "\n        self.high_availability_v3 = high_availability_core",
        1,
    )

# --------------------------------------------------
# Runtime version
# --------------------------------------------------

text = text.replace(
    'self.version = "3.5.0"',
    'self.version = "3.6.0"',
)

# --------------------------------------------------
# Service registration
# --------------------------------------------------

if "Aletheus High Availability Platform" not in text:

    anchor = 'self.services.register("Aletheus Observability Platform"'

    idx = text.find(anchor)

    if idx == -1:
        raise SystemExit("Observability service anchor not found.")

    end = text.find("\n", idx)

    service = '''

        self.services.register(
            "Aletheus High Availability Platform",
            {
                "status": "online",
                "version": self.high_availability_v3.VERSION,
            },
        )
'''

    text = text[:end+1] + service + text[end+1:]

# --------------------------------------------------
# Command registration
# --------------------------------------------------

if 'self.commands.register("ha.bootstrap"' not in text:

    anchor = 'self.commands.register("telemetry.statistics", self._cmd_telemetry_statistics)'

    if anchor not in text:
        raise SystemExit("Telemetry command anchor not found.")

    text = text.replace(
        anchor,
        anchor + '''

        # --------------------------------------------------
        # v3.6 High Availability
        # --------------------------------------------------

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
''',
        1,
    )

core.write_text(text)

print("✔ AletheusOS v3.6 runtime integration complete.")
