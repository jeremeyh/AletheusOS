"""
Event Bus Command Registration

Genesis 6
"""

def register_event_commands(runtime):

    commands = runtime.commands

    commands.register("event.bootstrap", runtime._cmd_event_bootstrap)
    commands.register("event.publish", runtime._cmd_event_publish)
    commands.register("event.subscribe", runtime._cmd_event_subscribe)
    commands.register("event.unsubscribe", runtime._cmd_event_unsubscribe)
    commands.register("event.history", runtime._cmd_event_history)
    commands.register("event.replay", runtime._cmd_event_replay)
    commands.register("event.statistics", runtime._cmd_event_statistics)
