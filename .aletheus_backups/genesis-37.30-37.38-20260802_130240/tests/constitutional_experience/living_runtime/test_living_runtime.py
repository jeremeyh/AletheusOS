import pytest

from aletheus.constitutional_experience.living_runtime.engine import (
    LivingExperienceEngine,
)
from aletheus.constitutional_experience.living_runtime.equations import (
    critical_damping,
    respiration_wave,
)
from aletheus.constitutional_experience.living_runtime.models import (
    AmbientField,
    ResonanceProfile,
    SpatialBody,
)


def test_equations():
    assert critical_damping(100, 1) == pytest.approx(20)
    assert respiration_wave(0) == pytest.approx(0.5)


def test_elastic_motion():
    b = SpatialBody("x", 1, 0, 0, 0)
    n = LivingExperienceEngine().step_body(b, (1, 0, 0), AmbientField(), 0.016)
    assert n.x > b.x


def test_crystalline_vitality():
    s = LivingExperienceEngine().vitality(
        coherence=0.99,
        stability=0.98,
        continuity=0.97,
        frame_ms=8,
        target_ms=8.333333,
        latency_ms=7.5,
        field=AmbientField(),
        profile=ResonanceProfile(0.15, 0.8, 1),
        t=1,
    )
    assert s.phase == "crystalline"
    assert s.meantime_quotient > 0.9
