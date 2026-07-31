class RuntimeMigrationReporter:
    def render(self, tracker):

        report = tracker.report()

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME MIGRATION TRACKER",
            "========================================================",
            "",
            f"Responsibilities...............{len(report.items)}",
            f"Completion.....................{tracker.completion()}%",
            "",
            "Migration Status",
        ]

        for item in report.items:
            lines.append(f"  [{item.status.upper()}] {item.name} -> {item.destination}")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
