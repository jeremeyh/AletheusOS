from aletheus.runtime.extraction_missions import (
    RuntimeExtractionMissionManager,
    RuntimeExtractionMissionReporter,
)


def main():

    manager = RuntimeExtractionMissionManager()

    manager.add(
        "RM-0001",
        "Health",
        "Platform Intelligence",
        65,
    )

    manager.add(
        "RM-0002",
        "Diagnostics",
        "Platform Intelligence",
        48,
    )

    manager.add(
        "RM-0003",
        "Runtime Pulse",
        "Lifecycle Manager",
        25,
    )

    manager.add(
        "RM-0004",
        "Compatibility",
        "Compatibility Manager",
        120,
    )

    manager.add(
        "RM-0005",
        "Boot Sequence",
        "Runtime Boot Pipeline",
        397,
    )

    print(RuntimeExtractionMissionReporter().render(manager))


if __name__ == "__main__":
    main()
