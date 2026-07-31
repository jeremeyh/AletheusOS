class ExecutiveKernelReporter:
    def render(self, kernel) -> str:
        health = kernel.health()

        lines = [
            "========================================================",
            "ALETHEUSOS EXECUTIVE KERNEL",
            "========================================================",
            "",
            f"Status.........................{health['status']}",
            f"Active Services................{len(health['active_services'])}",
            f"Active Missions................{len(health['active_missions'])}",
            "",
            "Services",
        ]

        if health["active_services"]:
            lines.extend([f"  - {item}" for item in health["active_services"]])
        else:
            lines.append("  None")

        lines.append("")
        lines.append("Missions")

        if health["active_missions"]:
            lines.extend([f"  - {item}" for item in health["active_missions"]])
        else:
            lines.append("  None")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
