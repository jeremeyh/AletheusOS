class RuntimeCircuitReporter:
    def render(self, manager) -> str:
        health = manager.health()

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME ANCHOR CIRCUITS",
            "========================================================",
            "",
            f"Status.........................{health['status']}",
            f"Registered Circuits............{health['registered_circuits']}",
            f"Active Circuits................{health['active_circuits']}",
            f"Activation Events..............{health['activation_events']}",
            "",
            "Circuits",
        ]

        if health["circuits"]:
            for name, circuit in health["circuits"].items():
                deps = ", ".join(circuit["dependencies"]) or "None"
                lines.append(
                    f"  - {name} [{circuit['status']}] -> {circuit['capability']} | deps: {deps}"
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
