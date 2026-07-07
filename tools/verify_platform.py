from aletheus.platform_verification import (
    PlatformVerificationReport,
    PlatformVerificationReporter,
    bootstrap_verification_registry,
)


def main():
    registry = bootstrap_verification_registry()

    report = PlatformVerificationReport(
        results=registry.run_all()
    )

    print(
        PlatformVerificationReporter().render(report)
    )


if __name__ == "__main__":
    main()
