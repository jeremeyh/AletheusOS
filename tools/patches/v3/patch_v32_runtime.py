from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "from aletheus.persistence_v3 import persistence_core" not in text:
    text = text.replace(
        "from aletheus.plugins_v3 import plugin_core\n",
        "from aletheus.plugins_v3 import plugin_core\n"
        "from aletheus.persistence_v3 import persistence_core\n",
    )

if "self.persistence_v3 = persistence_core" not in text:
    text = text.replace(
        "self.plugins_v3 = plugin_core",
        "self.plugins_v3 = plugin_core\n        self.persistence_v3 = persistence_core",
        1,
    )

text = text.replace('self.version = "3.1.0"', 'self.version = "3.2.0"')
text = text.replace('self.version = "3.0.0"', 'self.version = "3.2.0"')

if "Aletheus Persistence Engine" not in text:
    marker = 'self.services.register("Aletheus Plugin Manager"'
    idx = text.find(marker)
    if idx != -1:
        end = text.find("\n", idx)
        service = """

        self.services.register(
            "Aletheus Persistence Engine",
            {
                "status": "online",
                "version": self.persistence_v3.VERSION,
            },
        )
"""
        text = text[: end + 1] + service + text[end + 1 :]

if 'self.commands.register("state.bootstrap"' not in text:
    anchor = 'self.commands.register("plugin.statistics", self._cmd_plugin_statistics)'
    if anchor not in text:
        raise SystemExit("plugin.statistics anchor not found.")

    text = text.replace(
        anchor,
        anchor
        + """

        # v3.2 Persistence Engine
        self.commands.register("state.bootstrap", self._cmd_state_bootstrap)
        self.commands.register("state.save", self._cmd_state_save)
        self.commands.register("state.load", self._cmd_state_load)
        self.commands.register("state.snapshot", self._cmd_state_snapshot)
        self.commands.register("state.restore", self._cmd_state_restore)
        self.commands.register("state.export", self._cmd_state_export)
        self.commands.register("state.import", self._cmd_state_import)
        self.commands.register("state.statistics", self._cmd_state_statistics)
""",
        1,
    )

core.write_text(text)
print("✔ v3.2 persistence runtime integration patched.")
