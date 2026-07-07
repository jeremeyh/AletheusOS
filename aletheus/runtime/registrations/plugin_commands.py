"""
Plugin Command Registration

Genesis 6
"""

def register_plugin_commands(runtime):

    commands = runtime.commands

    commands.register("plugin.bootstrap", runtime._cmd_plugin_bootstrap)
    commands.register("plugin.install", runtime._cmd_plugin_install)
    commands.register("plugin.enable", runtime._cmd_plugin_enable)
    commands.register("plugin.disable", runtime._cmd_plugin_disable)
    commands.register("plugin.update", runtime._cmd_plugin_update)
    commands.register("plugin.remove", runtime._cmd_plugin_remove)
    commands.register("plugin.list", runtime._cmd_plugin_list)
    commands.register("plugin.status", runtime._cmd_plugin_status)
    commands.register("plugin.statistics", runtime._cmd_plugin_statistics)
