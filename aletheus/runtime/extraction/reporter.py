class RuntimeExtractionReporter:

    def render(self, plan):

        lines = [
            "========================================================",
            "ALETHEUSOS EXTRACTION PLAN",
            "========================================================",
            "",
            f"Candidates.....................{len(plan.candidates)}",
            "",
            "Migration Order",
        ]

        for item in plan.candidates:

            lines.append(
                f"{item.priority}. "
                f"{item.name}"
            )

            lines.append(
                f"   -> {item.destination}"
            )

            lines.append(
                f"   ~{item.estimated_lines} lines "
                f"(confidence {item.confidence})"
            )

        lines.extend([
            "",
            "========================================================",
        ])

        return "\n".join(lines)
