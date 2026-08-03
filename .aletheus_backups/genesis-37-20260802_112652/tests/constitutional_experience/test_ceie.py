from aletheus.constitutional_experience.ceie_core.engine import Engine
from aletheus.constitutional_experience.models import EvidenceSignal, ExperienceContext


def test_projection_reduced_motion():
    p = Engine().project(
        EvidenceSignal("e", 1, 1, 1, 0.7, 0.2),
        ExperienceContext("u", "m", 0.4, 0.5, True),
    )
    assert p.motion_scale == 0 and p.respiration_hz == 0 and p.provenance_required
