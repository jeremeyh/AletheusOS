from aletheus.runtime.boot_pipeline.manifest import BOOT_PHASES
from aletheus.runtime.boot_pipeline.report import BootReport


def main():

    report = BootReport()

    for phase in BOOT_PHASES:
        report.record(phase)

    report.finish()

    print("========================================================")
    print("ALETHEUSOS RUNTIME BOOT REPORT")
    print("========================================================")
    print()

    for phase in report.phases:
        print(f"✓ {phase}")

    print()
    print(f"Completed......................{report.completed}")
    print(f"Boot Phases....................{len(report.phases)}")
    print("========================================================")


if __name__ == "__main__":
    main()
