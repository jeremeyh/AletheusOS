from __future__ import annotations

from dataclasses import replace

from .models import MissionContext, NavigationContext


class Engine:
    def activate(
        self, navigation: NavigationContext, mission: MissionContext
    ) -> NavigationContext:
        if not mission.active:
            raise ValueError("Cannot activate an inactive mission")
        attrs = dict(navigation.attributes)
        attrs["mission"] = {
            "objective": mission.objective,
            "subject": mission.subject,
            "constraints": mission.constraints,
        }
        return replace(navigation, mission_id=mission.mission_id, attributes=attrs)

    def mission_summary(self, mission: MissionContext) -> dict[str, object]:
        return {
            "missionId": mission.mission_id,
            "objective": mission.objective,
            "subject": mission.subject,
            "constraints": mission.constraints,
            "active": mission.active,
        }
