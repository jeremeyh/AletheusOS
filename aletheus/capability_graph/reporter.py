class CapabilityGraphReporter:
    def render(self, graph):

        lines = [
            "========================================================",
            "ALETHEUSOS CAPABILITY GRAPH",
            "========================================================",
            "",
            f"Capabilities.............{graph.node_count()}",
            f"Relationships............{graph.edge_count()}",
            "",
        ]

        for node in graph.nodes.values():
            lines.append(node.name)

            deps = graph.dependencies(node.id)

            if deps:
                for dep in deps:
                    target = graph.nodes.get(dep)

                    if target:
                        lines.append(f"   -> {target.name}")

            lines.append("")

        lines.append("========================================================")

        return "\n".join(lines)
