from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# --------------------------------------------------
# Import
# --------------------------------------------------

if "from aletheus.federation_v3 import federation_core" not in text:
    text = text.replace(
        "from aletheus.event_bus_v3 import event_bus_core\n",
        "from aletheus.event_bus_v3 import event_bus_core\n"
        "from aletheus.federation_v3 import federation_core\n",
        1,
    )

# --------------------------------------------------
# Runtime initialization
# --------------------------------------------------

if "self.federation_v3 = federation_core" not in text:
    text = text.replace(
        "self.event_bus_v3 = event_bus_core",
        "self.event_bus_v3 = event_bus_core\n"
        "        self.federation_v3 = federation_core",
        1,
    )

# --------------------------------------------------
# Runtime version
# --------------------------------------------------

text = text.replace(
    'self.version = "3.3.0"',
    'self.version = "3.4.0"',
)

# --------------------------------------------------
# Service registration
# --------------------------------------------------

if "Aletheus Federated Knowledge Fabric" not in text:

    marker = 'self.services.register("Aletheus Event Bus"'

    idx = text.find(marker)

    if idx != -1:

        end = text.find("\n", idx)

        service = '''

        self.services.register(
            "Aletheus Federated Knowledge Fabric",
            {
                "status": "online",
                "version": self.federation_v3.VERSION,
            },
        )
'''

        text = text[:end+1] + service + text[end+1:]

# --------------------------------------------------
# Command registration
# --------------------------------------------------

if 'self.commands.register("federation.bootstrap"' not in text:

    anchor = 'self.commands.register("event.statistics", self._cmd_event_statistics)'

    if anchor not in text:
        raise SystemExit("event.statistics anchor not found.")

    text = text.replace(
        anchor,
        anchor + '''

        # v3.4 Federation
        self.commands.register("federation.bootstrap", self._cmd_federation_bootstrap)
        self.commands.register("federation.join", self._cmd_federation_join)
        self.commands.register("federation.leave", self._cmd_federation_leave)
        self.commands.register("federation.discover", self._cmd_federation_discover)
        self.commands.register("federation.query", self._cmd_federation_query)
        self.commands.register("federation.broadcast", self._cmd_federation_broadcast)
        self.commands.register("federation.statistics", self._cmd_federation_statistics)
''',
        1,
    )

core.write_text(text)

print("✔ v3.4 Federation runtime integrated.")
