from __future__ import annotations

import pytest

from aletheus.experience_gateway.models import (
    ExperienceConfidence,
    ExperienceMission,
)


def test_confidence_rejects_value_above_one() -> None:
    with pytest.raises(ValueError):
        ExperienceConfidence(
            value=1.1,
            label="high",
        )


def test_mission_rejects_progress_above_one_hundred() -> None:
    with pytest.raises(ValueError):
        ExperienceMission(
            id="mission",
            name="Mission",
            description="Invalid progress",
            state="active",
            progress=101,
        )
