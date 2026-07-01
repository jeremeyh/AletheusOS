"""
Application Command Registration

Version 4.7.5
"""


def register_application_commands(runtime):

    commands = runtime.commands

    commands.register(
        "application.register",
        runtime._cmd_application_register,
    )

    commands.register(
        "application.list",
        runtime._cmd_application_list,
    )

    commands.register(
        "application.start",
        runtime._cmd_application_start,
    )

    commands.register(
        "application.stop",
        runtime._cmd_application_stop,
    )

    commands.register(
        "application.restart",
        runtime._cmd_application_restart,
    )

    commands.register(
        "application.health",
        runtime._cmd_application_health,
    )

    commands.register(
        "application.stats",
        runtime._cmd_application_stats,
    )

    commands.register(
        "application.install",
        runtime._cmd_application_install,
    )

    commands.register(
        "application.uninstall",
        runtime._cmd_application_uninstall,
    )

    commands.register(
        "application.manifest",
        runtime._cmd_application_manifest,
    )

    commands.register(
        "application.events",
        runtime._cmd_application_events,
    )

    commands.register(
        "application.bootstrap.defaults",
        runtime._cmd_application_bootstrap_defaults,
    )
