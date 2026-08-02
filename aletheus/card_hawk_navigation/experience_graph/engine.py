from __future__ import annotations

from collections import defaultdict, deque
from typing import ClassVar

from .models import ExperienceEdge, ExperienceNode


class Engine:
    NODES: ClassVar[tuple[ExperienceNode, ...]] = (
        ExperienceNode("locker_room", "Locker Room™", "locker_room"),
        ExperienceNode("vault", "Vault™", "vault"),
        ExperienceNode("gallery", "Gallery™", "gallery"),
        ExperienceNode("scoreboard", "Scoreboard™", "scoreboard"),
        ExperienceNode("field_vision", "Field Vision™", "field_vision"),
        ExperienceNode("mission_control", "Mission Control™", "mission_control"),
        ExperienceNode("war_room", "War Room™", "war_room"),
        ExperienceNode("scouting_report", "Scouting Report™", "scouting_report"),
        ExperienceNode("game_film", "Game Film™", "game_film"),
        ExperienceNode("marketplace", "Marketplace™", "marketplace"),
        ExperienceNode("observatory", "Observatory™", "observatory", "OVERLAY_SURFACE"),
    )
    EDGES: ClassVar[tuple[ExperienceEdge, ...]] = (
        ExperienceEdge("locker_room", "vault", "OWNS"),
        ExperienceEdge("locker_room", "scoreboard", "REVIEWS"),
        ExperienceEdge("locker_room", "mission_control", "OPERATES"),
        ExperienceEdge("vault", "gallery", "PRESENTS"),
        ExperienceEdge("vault", "scouting_report", "INSPECTS"),
        ExperienceEdge("field_vision", "scouting_report", "INVESTIGATES"),
        ExperienceEdge("field_vision", "war_room", "ESCALATES"),
        ExperienceEdge("scouting_report", "war_room", "DECIDES"),
        ExperienceEdge("game_film", "war_room", "INFORMS"),
        ExperienceEdge("war_room", "marketplace", "COMMITS"),
        ExperienceEdge("mission_control", "field_vision", "MONITORS"),
        ExperienceEdge("observatory", "field_vision", "HYDRATES"),
    )

    def route(self, source: str, destination: str) -> tuple[str, ...]:
        a: dict[str, list[str]] = defaultdict(list)
        for e in self.EDGES:
            a[e.source].append(e.destination)
        q = deque([(source, (source,))])
        seen = {source}
        while q:
            cur, path = q.popleft()
            if cur == destination:
                return path
            for nxt in a[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, path + (nxt,)))
        raise KeyError(f"No experience route from {source} to {destination}")
