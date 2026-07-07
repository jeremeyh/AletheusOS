from aletheus.runtime.lifecycle import (
    RuntimeLifecycleManager,
    RuntimeLifecycleReporter,
)


def main():

    lifecycle = RuntimeLifecycleManager()

    lifecycle.transition(
        "booting",
        "Boot Pipeline started",
    )

    lifecycle.transition(
        "ready",
        "Boot Pipeline completed",
    )

    lifecycle.transition(
        "running",
        "Runtime accepted control",
    )

    print(
        RuntimeLifecycleReporter().render(
            lifecycle
        )
    )


if __name__ == "__main__":
    main()
