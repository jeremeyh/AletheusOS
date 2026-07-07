from aletheus.runtime.commands_v2 import (
    RuntimeCommandRegistry,
    RuntimeCommandRegistryReporter,
)


def main():

    registry = RuntimeCommandRegistry()

    registry.register(
        name="runtime.health",
        category="runtime",
        description="Return runtime health.",
        handler=lambda payload: {
            "runtime": "healthy",
            "payload": payload,
        },
    )

    registry.register(
        name="runtime.boot",
        category="lifecycle",
        description="Execute runtime boot sequence.",
        handler=lambda payload: {
            "boot": "accepted",
            "payload": payload,
        },
    )

    registry.register(
        name="platform.verify",
        category="verification",
        description="Run platform verification.",
        handler=lambda payload: {
            "verification": "pass",
            "payload": payload,
        },
    )

    registry.dispatch(
        "runtime.health",
        {"source": "tool"},
    )

    print(
        RuntimeCommandRegistryReporter().render(
            registry
        )
    )


if __name__ == "__main__":
    main()
