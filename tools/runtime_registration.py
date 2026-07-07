from aletheus.runtime.registration import (
    RuntimeRegistrationManager,
    RuntimeRegistrationReporter,
)


def main():

    manager = RuntimeRegistrationManager()

    manager.register("service", "Executive Kernel")
    manager.register("service", "Runtime Service Mesh")
    manager.register("service", "Relay Network")
    manager.register("service", "Catalyst")

    manager.register("registry", "Runtime Registry")
    manager.register("registry", "Intent Registry")

    manager.register("application", "Card Hawk")

    print(
        RuntimeRegistrationReporter().render(
            manager
        )
    )


if __name__ == "__main__":
    main()
