class RuntimeServiceMeshReporter:
    def render(self, mesh) -> str:
        health = mesh.health()

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME SERVICE MESH",
            "========================================================",
            "",
            f"Status.........................{health['status']}",
            f"Registered Nodes...............{health['nodes']}",
            f"Registered Handlers............{health['handlers']}",
            f"Routes Processed...............{health['routes_processed']}",
            "",
            "Nodes",
        ]

        if health["node_names"]:
            lines.extend([f"  - {node}" for node in health["node_names"]])
        else:
            lines.append("  None")

        lines.extend([
            "",
            "========================================================",
        ])

        return "\n".join(lines)
