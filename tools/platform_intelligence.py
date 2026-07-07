from aletheus.platform_intelligence import (
    PlatformIntelligenceEngine,
    PlatformIntelligenceReporter,
)


def main():
    report = PlatformIntelligenceEngine(".").evaluate()
    print(PlatformIntelligenceReporter().render(report))
    raise SystemExit(0 if report.passed() else 1)


if __name__ == "__main__":
    main()
