class RuntimeCompressionReporter:
    def render(self, report):

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME COMPRESSION",
            "========================================================",
            "",
            f"Original Core Lines.............{report.original_lines}",
            f"Current Core Lines..............{report.current_lines}",
            f"Lines Removed...................{report.lines_removed}",
            f"Compression.....................{report.compression_percent}%",
            "",
            f"Responsibilities...............{report.responsibilities_complete}/{report.responsibilities_total}",
            f"Completion......................{report.completion_percent}%",
            "",
            f"Platform Health.................{report.platform_health}%",
            "",
            "========================================================",
        ]

        return "\n".join(lines)
