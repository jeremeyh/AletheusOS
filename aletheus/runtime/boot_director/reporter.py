class RuntimeBootDirectorReporter:
    def render(self, report):
        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME BOOT DIRECTOR",
            "========================================================",
            "",
            f"Status.........................{report['status']}",
            f"Phases.........................{len(report['phases'])}",
            "",
            "Boot Phases",
        ]

        for phase in report["phases"]:
            lines.append(f"  - [{phase['status'].upper()}] {phase['phase']}")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
