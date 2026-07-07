def register(runtime):

    runtime.commands.register(
        "runtime.status",
        runtime._cmd_status,
    )

    runtime.commands.register(
        "runtime.version",
        runtime._cmd_version,
    )

    runtime.commands.register(
        "runtime.metrics",
        runtime._cmd_metrics,
    )

    runtime.commands.register(
        "runtime.health",
        runtime._cmd_health,
    )

    runtime.commands.register(
        "runtime.diagnostics",
        runtime._cmd_diagnostics,
    )

    runtime.commands.register(
        "runtime.statistics",
        runtime._cmd_statistics,
    )

    runtime.commands.register(
        "runtime.services",
        runtime._cmd_services,
    )

    runtime.commands.register(
        "runtime.commands",
        runtime._cmd_commands,
    )
