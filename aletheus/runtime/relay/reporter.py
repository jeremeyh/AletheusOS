class RelayNetworkReporter:
    def render(self, network) -> str:
        health = network.health()

        lines = [
            "========================================================",
            "ALETHEUSOS RUNTIME RELAY NETWORK",
            "========================================================",
            "",
            f"Status.........................{health['status']}",
            f"Registered Routes..............{len(health['routes'])}",
            f"Packets Processed..............{health['history_count']}",
            "",
            "Routes",
        ]

        if health["routes"]:
            lines.extend([f"  - {route}" for route in health["routes"]])
        else:
            lines.append("  None")

        lines.extend([
            "",
            "========================================================",
        ])

        return "\n".join(lines)
