class RuntimeCompositionReporter:
    def render(self, composition):

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME COMPOSITION ROOT",
            "========================================================",
            "",
            f"Services........................{len(composition.services)}",
            "",
            "Runtime Services",
        ]

        for name in sorted(composition.services):
            lines.append(f"  - {name}")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
