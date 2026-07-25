from aletheus.runtime import runtime_core

print("=== Genesis 7 Validation ===")


print(
    {
        "commands":
            runtime_core.commands.count(),

        "health":
            runtime_core.health(),

        "genesis6":
            runtime_core.genesis6_validate(),

        "freeze":
            runtime_core.genesis6_freeze_review(),

        "runtime_facade":
            type(
                runtime_core.runtime_facade
            ).__name__
    }
)
