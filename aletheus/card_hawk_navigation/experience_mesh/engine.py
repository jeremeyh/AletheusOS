from __future__ import annotations

from collections import defaultdict
from typing import ClassVar

from .models import ExperienceEdge, ExperienceNode


class Engine:
    CORE_NODES: ClassVar[tuple[ExperienceNode, ...]] = (
        ExperienceNode("locker_room", "Locker Room™", "locker_room"),
        ExperienceNode("vault", "Vault™", "vault"),
        ExperienceNode("gallery", "Gallery™", "gallery"),
        ExperienceNode("scoreboard", "Scoreboard™", "scoreboard"),
        ExperienceNode("field_vision", "Field Vision™", "field_vision"),
        ExperienceNode("mission_control", "Mission Control™", "mission_control"),
        ExperienceNode("war_room", "War Room™", "war_room"),
        ExperienceNode("marketplace", "Marketplace™", "marketplace"),
        ExperienceNode("observatory", "Observatory™", "observatory"),
        ExperienceNode("scouting_report", "Scouting Report™", "scouting_report"),
        ExperienceNode("game_film", "Game Film™", "game_film"),
    )
    CORE_EDGES: ClassVar[tuple[ExperienceEdge, ...]] = (
        ExperienceEdge("locker_room", "vault", "OWNS"),
        ExperienceEdge("vault", "gallery", "PRESENTS"),
        ExperienceEdge("field_vision", "scouting_report", "INVESTIGATES"),
        ExperienceEdge("scouting_report", "war_room", "ESCALATES"),
        ExperienceEdge("game_film", "war_room", "INFORMS"),
        ExperienceEdge("war_room", "marketplace", "COMMITS"),
        ExperienceEdge("mission_control", "field_vision", "MONITORS"),
        ExperienceEdge("observatory", "field_vision", "HYDRATES"),
        ExperienceEdge("scoreboard", "war_room", "REBALANCES"),
        ExperienceEdge("marketplace", "vault", "SETTLES"),
    )

    def neighbors(self, node_id: str) -> tuple[str, ...]:
        a: dict[str, list[str]] = defaultdict(list)
        for e in self.CORE_EDGES:
            a[e.source].append(e.destination)
            a[e.destination].append(e.source)
        return tuple(sorted(dict.fromkeys(a[node_id])))

    def describe(self) -> dict[str, object]:
        return {
            "nodeCount": len(self.CORE_NODES),
            "edgeCount": len(self.CORE_EDGES),
            "nodes": tuple(n.node_id for n in self.CORE_NODES),
        }
