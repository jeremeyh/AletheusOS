from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

anchor = 'self.commands.register("cluster.statistics", self._cmd_cluster_statistics)'

block = '''
        # Plugin Manager
        self.commands.register("plugin.bootstrap", self._cmd_plugin_bootstrap)
        self.commands.register("plugin.install", self._cmd_plugin_install)
        self.commands.register("plugin.enable", self._cmd_plugin_enable)
        self.commands.register("plugin.disable", self._cmd_plugin_disable)
        self.commands.register("plugin.update", self._cmd_plugin_update)
        self.commands.register("plugin.remove", self._cmd_plugin_remove)
        self.commands.register("plugin.list", self._cmd_plugin_list)
        self.commands.register("plugin.status", self._cmd_plugin_status)
        self.commands.register("plugin.statistics", self._cmd_plugin_statistics)
'''

if 'self.commands.register("plugin.bootstrap"' not in text:
    text = text.replace(anchor, anchor + "\n" + block, 1)

p.write_text(text)

print("✔ Plugin commands registered.")
