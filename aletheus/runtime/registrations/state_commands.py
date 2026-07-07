"""
State / Persistence Command Registration

Genesis 6
"""

def register_state_commands(runtime):

    commands = runtime.commands

    commands.register("state.bootstrap", runtime._cmd_state_bootstrap)
    commands.register("state.save", runtime._cmd_state_save)
    commands.register("state.load", runtime._cmd_state_load)
    commands.register("state.snapshot", runtime._cmd_state_snapshot)
    commands.register("state.restore", runtime._cmd_state_restore)
    commands.register("state.export", runtime._cmd_state_export)
    commands.register("state.import", runtime._cmd_state_import)
    commands.register("state.statistics", runtime._cmd_state_statistics)
