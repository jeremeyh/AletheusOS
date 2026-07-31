class RuntimeExtractionMissionReporter:
    def render(self, manager):

        health = manager.health()

        lines = [
            "========================================================",
            "ALETHEUSOS EXTRACTION MISSIONS",
            "========================================================",
            "",
            f"Missions.......................{health['missions']}",
            f"Completion.....................{health['completion']}%",
            "",
            "Mission Queue",
        ]

        for mission in manager.missions:
            lines.append(f"[{mission.status.upper()}] {mission.mission_id}")

            lines.append(f"  {mission.responsibility}")

            lines.append(f"  -> {mission.destination}")

            lines.append(f"  ~{mission.estimated_lines} lines")

        lines.extend(
            [
                "",
                "========================================================",
            ]
        )

        return "\n".join(lines)
