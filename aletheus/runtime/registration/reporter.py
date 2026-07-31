class RuntimeRegistrationReporter:
    def render(self, manager):

        health = manager.health()

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME REGISTRATION MANAGER",
            "========================================================",
            "",
            f"Categories.....................{len(health['categories'])}",
            f"Registrations..................{health['registration_count']}",
            "",
            "Registration Categories",
        ]

        if health["categories"]:
            for category in health["categories"]:
                lines.append(f"  - {category}")
        else:
            lines.append("  None")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
