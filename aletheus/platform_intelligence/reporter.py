from .models import ArchitecturalFitnessReport


class PlatformIntelligenceReporter:
    def render(self, report: ArchitecturalFitnessReport) -> str:
        lines = [
            "========================================================",
            "ALETHEUSOS PLATFORM INTELLIGENCE",
            "========================================================",
            "",
            f"Status...........................{report.status}",
            f"Architectural Fitness Score......{report.score}%",
            "",
            f"Subsystems Discovered............{report.subsystem_count}",
            f"Python Files Scanned.............{report.python_file_count}",
            "",
            "Oversized Files",
        ]

        if report.oversized_files:
            lines.extend([f"  - {item}" for item in report.oversized_files])
        else:
            lines.append("  None")

        lines.append("")
        lines.append("Duplicate Risk")

        if report.duplicate_risk:
            lines.extend([f"  - {item}" for item in report.duplicate_risk])
        else:
            lines.append("  None")

        lines.extend(
            [
                "",
                "Timestamp",
                report.created_at,
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
