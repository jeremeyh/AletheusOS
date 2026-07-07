class CoreLifecycleBridgeReporter:

    def render(self, report):

        lines = [
            "========================================================",
            "ALETHEUSOS CORE LIFECYCLE BRIDGE",
            "========================================================",
            "",
            f"Status.........................{report.status}",
            f"Lifecycle State................{report.lifecycle_state}",
            f"Boot Status....................{report.boot_status}",
            "",
            "Delegated Services",
        ]

        if report.services:
            for service in report.services:
                lines.append(f"  - {service}")
        else:
            lines.append("  None")

        lines.extend([
            "",
            "========================================================",
        ])

        return "\n".join(lines)
