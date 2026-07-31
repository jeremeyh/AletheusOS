class CatalystReporter:
    def render(self, report) -> str:
        lines = [
            "========================================================",
            "ALETHEUSOS CATALYST OPTIMIZATION REPORT",
            "========================================================",
            "",
            f"Status.........................{report.status}",
            f"Optimized Routes...............{len(report.optimized_routes)}",
            f"Recommendations................{len(report.recommendations)}",
            "",
            "Optimized Routes",
        ]

        if report.optimized_routes:
            lines.extend([f"  - {route}" for route in report.optimized_routes])
        else:
            lines.append("  None")

        lines.append("")
        lines.append("Recommendations")

        if report.recommendations:
            for rec in report.recommendations:
                lines.append(
                    f"  - [{rec.impact.upper()}] {rec.target}: {rec.recommendation}"
                )
        else:
            lines.append("  None")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
