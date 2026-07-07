class RuntimeLifecycleReporter:

    def render(self, manager):

        health = manager.health()

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME LIFECYCLE",
            "========================================================",
            "",
            f"Current State.................{health['current_state']}",
            f"Transitions...................{health['transition_count']}",
            "",
            "History",
        ]

        if health["history"]:
            for item in health["history"]:
                lines.append(
                    f"  {item['from']} -> {item['to']} ({item['reason']})"
                )
        else:
            lines.append("  None")

        lines.extend([
            "",
            "========================================================",
        ])

        return "\n".join(lines)
