class RuntimeCoreDecompositionReporter:
    def render(self, plan) -> str:
        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME CORE DECOMPOSITION PLAN",
            "========================================================",
            "",
            f"Core Path........................{plan.core.path}",
            f"Line Count.......................{plan.core.line_count}",
            f"Functions........................{plan.core.function_count}",
            f"Classes..........................{plan.core.class_count}",
            f"Imports..........................{plan.core.import_count}",
            "",
            f"Responsibilities Identified......{len(plan.findings)}",
            f"Runtime Compression Index........{plan.runtime_compression_index}%",
            "",
            "Responsibility Migration Map",
        ]

        if plan.findings:
            for finding in plan.findings:
                lines.append(
                    f"  - {finding.responsibility}: {finding.matches} signals "
                    f"-> {finding.suggested_destination} "
                    f"(confidence {finding.confidence})"
                )
        else:
            lines.append("  None")

        lines.append("")
        lines.append("Largest Functions")

        if plan.core.largest_functions:
            for fn in plan.core.largest_functions:
                lines.append(
                    f"  - {fn['name']} at line {fn['line']} ({fn['size']} lines)"
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
