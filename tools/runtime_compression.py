from aletheus.runtime.compression import (
    RuntimeCompressionDashboard,
    RuntimeCompressionReporter,
)


def main():

    dashboard = RuntimeCompressionDashboard()

    report = dashboard.report(
        completed=2,
        health=100.0,
    )

    print(
        RuntimeCompressionReporter().render(
            report
        )
    )


if __name__ == "__main__":
    main()
