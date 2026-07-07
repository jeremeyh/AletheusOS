from aletheus.runtime.extraction import (
    RuntimeExtractionPlanner,
    RuntimeExtractionReporter,
)


def main():

    planner = RuntimeExtractionPlanner()

    plan = planner.build()

    print(
        RuntimeExtractionReporter().render(
            plan
        )
    )


if __name__ == "__main__":
    main()
