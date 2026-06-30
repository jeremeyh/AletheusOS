from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# ----------------------------------------------------
# Import
# ----------------------------------------------------
if "from aletheus.plugins_v3 import plugin_core" not in text:
    marker = "from aletheus.distributed_v3 import distributed_v3_core\n"
    if marker in text:
        text = text.replace(
            marker,
            marker + "from aletheus.plugins_v3 import plugin_core\n",
            1,
        )

# ----------------------------------------------------
# Runtime object
# ----------------------------------------------------
if "self.plugins_v3 = plugin_core" not in text:
    if "self.distributed = distributed_v3_core" in text:
        text = text.replace(
            "self.distributed = distributed_v3_core",
            "self.distributed = distributed_v3_core\n"
            "        self.plugins_v3 = plugin_core",
            1,
        )

# ----------------------------------------------------
# Service Registration
# ----------------------------------------------------
if '"Aletheus Plugin Manager"' not in text:
    anchor = 'self.services.register("Aletheus Distributed Runtime Fabric"'
    idx = text.find(anchor)
    if idx != -1:
        end = text.find("\n", idx)
        insertion = '''

        self.services.register(
            "Aletheus Plugin Manager",
            {
                "status": "online",
                "version": getattr(self.plugins_v3, "VERSION", "3.1.0"),
            },
        )
'''
        text = text[:end+1] + insertion + text[end+1:]

# ----------------------------------------------------
# Command Registration
# ----------------------------------------------------
if 'self.commands.register("plugin.bootstrap"' not in text:

    anchor = 'self.commands.register("cluster.statistics", self._cmd_cluster_statistics)'

    if anchor in text:
        text = text.replace(
            anchor,
            anchor + '''

        # v3.1 Plugin Framework
        self.commands.register("plugin.bootstrap", self._cmd_plugin_bootstrap)
        self.commands.register("plugin.install", self._cmd_plugin_install)
        self.commands.register("plugin.enable", self._cmd_plugin_enable)
        self.commands.register("plugin.disable", self._cmd_plugin_disable)
        self.commands.register("plugin.update", self._cmd_plugin_update)
        self.commands.register("plugin.remove", self._cmd_plugin_remove)
        self.commands.register("plugin.list", self._cmd_plugin_list)
        self.commands.register("plugin.status", self._cmd_plugin_status)
        self.commands.register("plugin.statistics", self._cmd_plugin_statistics)
''',
            1,
        )

core.write_text(text)

print("✔ v3.1 runtime registration completed.")
