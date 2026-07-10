"""
Event Command Registration

Genesis 7

Uses EventCommandAdapter boundary.
"""


def register_event_commands(runtime):

    commands = runtime.commands


    commands.register(
        "event.bootstrap",
        runtime.event_adapter.bootstrap,
    )


    commands.register(
        "event.publish",
        runtime.event_adapter.publish,
    )


    commands.register(
        "event.subscribe",
        runtime.event_adapter.subscribe,
    )


    commands.register(
        "event.unsubscribe",
        runtime.event_adapter.unsubscribe,
    )


    commands.register(
        "event.history",
        runtime.event_adapter.history,
    )


    commands.register(
        "event.replay",
        runtime.event_adapter.replay,
    )


    commands.register(
        "event.statistics",
        runtime.event_adapter.statistics,
    )
