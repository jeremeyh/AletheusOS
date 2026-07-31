class CapabilityManifestReporter:
    def render(self, registry):

        health = registry.health()

        lines = [
            "========================================================",
            "ALETHEUSOS CAPABILITY MANIFEST",
            "========================================================",
            "",
            f"Status.........................{health['status']}",
            f"Capabilities...................{health['capabilities']}",
            "",
            "Capability Catalog",
        ]

        for manifest in registry.all():
            lines.append(f"  - {manifest.id} ({manifest.provider})")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
