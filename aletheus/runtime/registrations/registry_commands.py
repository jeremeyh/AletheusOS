def register_registry_commands(runtime):

    commands = runtime.commands

    commands.register(
        "registry.snapshot",
        lambda context: context.add_result("registry", runtime.registry.snapshot()),
    )

    commands.register(
        "registry.domains",
        lambda context: context.add_result(
            "domains", list(runtime.registry.domains.keys())
        ),
    )

    commands.register(
        "registry.services",
        lambda context: context.add_result(
            "services", list(runtime.registry.services.keys())
        ),
    )

    commands.register(
        "registry.components",
        lambda context: context.add_result(
            "components", list(runtime.registry.components.keys())
        ),
    )

    commands.register(
        "registry.health",
        lambda context: context.add_result(
            "registry_health",
            {
                "healthy": True,
                "snapshot": runtime.registry.snapshot(),
            },
        ),
    )
