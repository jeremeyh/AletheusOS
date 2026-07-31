class RuntimeCommandRegistryReporter:
    def render(self, registry):

        health = registry.health()

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME COMMAND REGISTRY",
            "========================================================",
            "",
            f"Status.........................{health['status']}",
            f"Commands.......................{health['commands']}",
            f"Categories.....................{len(health['categories'])}",
            "",
            "Command Categories",
        ]

        if health["categories"]:
            for category in health["categories"]:
                lines.append(f"  - {category}")
        else:
            lines.append("  None")

        lines.append("")
        lines.append("Commands")

        if health["command_names"]:
            for command in health["command_names"]:
                lines.append(f"  - {command}")
        else:
            lines.append("  None")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
