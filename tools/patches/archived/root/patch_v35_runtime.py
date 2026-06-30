from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# --------------------------------------------------
# Import
# --------------------------------------------------

if "from aletheus.telemetry_v3 import telemetry_core" not in text:
    text = text.replace(
        "from aletheus.federation_v3 import federation_core\n",
        "from aletheus.federation_v3 import federation_core\n"
        "from aletheus.telemetry_v3 import telemetry_core\n",
        1,
    )

# --------------------------------------------------
# Runtime initialization
# --------------------------------------------------

if "self.telemetry_v3 = telemetry_core" not in text:
    text = text.replace(
        "self.federation_v3 = federation_core",
        "self.federation_v3 = federation_core\n"
        "        self.telemetry_v3 = telemetry_core",
        1,
    )

# --------------------------------------------------
# Runtime version
# --------------------------------------------------

text = text.replace(
    'self.version = "3.4.0"',
    'self.version = "3.5.0"',
)

# --------------------------------------------------
# Service registration
# --------------------------------------------------

if "Aletheus Observability Platform" not in text:

    marker = 'self.services.register("Aletheus Federated Knowledge Fabric"'

    idx = text.find(marker)

    if idx != -1:

        end = text.find("\n", idx)

        service = '''

        self.services.register(
            "Aletheus Observability Platform",
            {
                "status": "online",
                "version": self.telemetry_v3.VERSION,
            },
        )
'''

        text = text[:end+1] + service + text[end+1:]

# --------------------------------------------------
# Command registration
# --------------------------------------------------

if 'self.commands.register("telemetry.bootstrap"' not in text:

    anchor = 'self.commands.register("federation.statistics", self._cmd_federation_statistics)'

    if anchor not in text:
        raise SystemExit("federation.statistics anchor not found.")

    text = text.replace(
        anchor,
        anchor + '''

        # v3.5 Observability Platform
        self.commands.register("telemetry.bootstrap", self._cmd_telemetry_bootstrap)
        self.commands.register("telemetry.record", self._cmd_telemetry_record)
        self.commands.register("telemetry.metric", self._cmd_telemetry_metric)
        self.commands.register("telemetry.log", self._cmd_telemetry_log)
        self.commands.register("telemetry.trace", self._cmd_telemetry_trace)
        self.commands.register("telemetry.health", self._cmd_telemetry_health)
        self.commands.register("telemetry.timeline", self._cmd_telemetry_timeline)
        self.commands.register("telemetry.statistics", self._cmd_telemetry_statistics)
''',
        1,
    )

core.write_text(text)

print("✔ v3.5 Telemetry runtime integrated.")
