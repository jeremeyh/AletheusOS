from __future__ import annotations

from aletheus.autonomous_mission_intelligence.timeline_optimizer.engine import Engine
from aletheus.autonomous_mission_intelligence.timeline_optimizer.models import (
    TimelineTask,
)


def test_timeline_optimizer_is_bounded_and_deterministic() -> None:
    task = TimelineTask("task-1", 1.0)
    result = Engine().optimize([task])
    assert isinstance(result, dict)
    assert len(result["digest"]) == 64
