from aletheus.runtime.boot_director import (
    RuntimeBootDirector,
    RuntimeBootDirectorReporter,
)


class DemoRuntime:
    version = "demo"


def runtime_state_phase(runtime):
    return {
        "version": runtime.version,
        "status": "online",
    }


def command_phase(runtime):
    return {
        "commands": "registered",
    }


def service_phase(runtime):
    return {
        "services": "registered",
    }


def main():
    director = RuntimeBootDirector()

    director.register_phase(
        "runtime_state",
        runtime_state_phase,
    )

    director.register_phase(
        "commands",
        command_phase,
    )

    director.register_phase(
        "services",
        service_phase,
    )

    report = director.run(DemoRuntime())

    print(
        RuntimeBootDirectorReporter().render(
            report
        )
    )


if __name__ == "__main__":
    main()
