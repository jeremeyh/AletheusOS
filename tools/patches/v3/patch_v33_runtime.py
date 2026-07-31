from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Import
if "from aletheus.event_bus_v3 import event_bus_core" not in text:
    text = text.replace(
        "from aletheus.persistence_v3 import persistence_core\n",
        "from aletheus.persistence_v3 import persistence_core\n"
        "from aletheus.event_bus_v3 import event_bus_core\n",
        1,
    )

# Runtime initialization
if "self.event_bus_v3 = event_bus_core" not in text:
    text = text.replace(
        "self.persistence_v3 = persistence_core",
        "self.persistence_v3 = persistence_core\n"
        "        self.event_bus_v3 = event_bus_core",
        1,
    )

# Version
text = text.replace('self.version = "3.2.0"', 'self.version = "3.3.0"')

# Service
if "Aletheus Event Bus" not in text:
    marker = 'self.services.register("Aletheus Persistence Engine"'
    idx = text.find(marker)

    if idx != -1:
        end = text.find("\n", idx)
        service = """

        self.services.register(
            "Aletheus Event Bus",
            {
                "status": "online",
                "version": self.event_bus_v3.VERSION,
            },
        )
"""
        text = text[: end + 1] + service + text[end + 1 :]

# Commands
if 'self.commands.register("event.bootstrap"' not in text:
    anchor = 'self.commands.register("state.statistics", self._cmd_state_statistics)'

    if anchor not in text:
        raise SystemExit("state.statistics anchor not found.")

    text = text.replace(
        anchor,
        anchor
        + """

        # v3.3 Event Bus
        self.commands.register("event.bootstrap", self._cmd_event_bootstrap)
        self.commands.register("event.publish", self._cmd_event_publish)
        self.commands.register("event.subscribe", self._cmd_event_subscribe)
        self.commands.register("event.unsubscribe", self._cmd_event_unsubscribe)
        self.commands.register("event.history", self._cmd_event_history)
        self.commands.register("event.replay", self._cmd_event_replay)
        self.commands.register("event.statistics", self._cmd_event_statistics)
""",
        1,
    )

core.write_text(text)
print("✔ v3.3 Event Bus runtime integration patched.")
