class IntentRegistryReporter:
    def render(self, registry) -> str:
        records = registry.all()

        lines = [
            "========================================================",
            "ALETHEUSOS INTENT REGISTRY",
            "========================================================",
            "",
            f"Subsystems Registered............{len(records)}",
            "",
        ]

        for record in records:
            lines.extend(
                [
                    f"{record.name}",
                    f"  ID: {record.id}",
                    f"  Layer: {record.owner_layer}",
                    f"  Purpose: {record.purpose}",
                    f"  Capabilities: {', '.join(record.capabilities) or 'None'}",
                    f"  Dependencies: {', '.join(record.dependencies) or 'None'}",
                    f"  Outputs: {', '.join(record.outputs) or 'None'}",
                    "",
                ]
            )

        lines.append("========================================================")
        return "\n".join(lines)
