from aletheus.runtime.migration import (
    RuntimeMigrationReporter,
    RuntimeMigrationTracker,
)


def main():

    tracker = RuntimeMigrationTracker()

    tracker.add(
        "Boot Sequence",
        "Runtime Boot Pipeline",
        "complete",
    )

    tracker.add(
        "Lifecycle",
        "Runtime Lifecycle Manager",
        "complete",
    )

    tracker.add(
        "Registration",
        "Runtime Registration Manager",
        "complete",
    )

    tracker.add(
        "Commands",
        "Runtime Command Registry",
        "complete",
    )

    tracker.add(
        "Runtime Composition",
        "Runtime Composition Root",
        "complete",
    )

    tracker.add(
        "Legacy Boot()",
        "Boot Pipeline",
        "planned",
    )

    tracker.add(
        "Legacy Registration",
        "Registration Manager",
        "planned",
    )

    tracker.add(
        "Legacy Command Dispatch",
        "Command Registry",
        "planned",
    )

    print(
        RuntimeMigrationReporter().render(
            tracker
        )
    )


if __name__ == "__main__":
    main()
