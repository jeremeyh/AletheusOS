class RuntimeCoreShimReporter:

    def render(self, report):

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME CORE SHIM",
            "========================================================",
            "",
            f"Status.........................{report.status}",
            "",
            "Delegated Services",
        ]

        for service in report.delegated_services:
            lines.append(f"  - {service}")

        lines.extend([
            "",
            "========================================================",
        ])

        return "\n".join(lines)
