class RuntimeBootPipelineReporter:
    def render(self, report) -> str:
        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME BOOT PIPELINE",
            "========================================================",
            "",
            f"Status.........................{report.status}",
            f"Stages.........................{len(report.stages)}",
            "",
            "Boot Stages",
        ]

        if report.stages:
            for stage in report.stages:
                lines.append(
                    f"  - [{stage.status.upper()}] {stage.order}. {stage.name}"
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
