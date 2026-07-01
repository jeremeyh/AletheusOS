"""
Memory Command Registration

Version 4.6.2
"""

def register_memory_commands(runtime):

    commands = runtime.commands

    commands.register(
        "memory.remember",
        runtime._cmd_memory_remember,
    )

    commands.register(
        "memory.recall",
        runtime._cmd_memory_recall,
    )

    commands.register(
        "memory.stats",
        runtime._cmd_memory_stats,
    )

    commands.register(
        "memory.clear_working",
        runtime._cmd_memory_clear_working,
    )
