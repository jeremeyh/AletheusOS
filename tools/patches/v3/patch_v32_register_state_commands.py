from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

anchor = 'self.commands.register("plugin.statistics", self._cmd_plugin_statistics)'

block = """
        # =====================================================
        # v3.2 Persistence Engine
        # =====================================================
        self.commands.register("state.bootstrap", self._cmd_state_bootstrap)
        self.commands.register("state.save", self._cmd_state_save)
        self.commands.register("state.load", self._cmd_state_load)
        self.commands.register("state.snapshot", self._cmd_state_snapshot)
        self.commands.register("state.restore", self._cmd_state_restore)
        self.commands.register("state.export", self._cmd_state_export)
        self.commands.register("state.import", self._cmd_state_import)
        self.commands.register("state.statistics", self._cmd_state_statistics)
"""

if 'self.commands.register("state.bootstrap"' not in text:
    if anchor not in text:
        raise SystemExit("Plugin registration anchor not found.")
    text = text.replace(anchor, anchor + "\n" + block, 1)

p.write_text(text)
print("✔ State commands registered.")
