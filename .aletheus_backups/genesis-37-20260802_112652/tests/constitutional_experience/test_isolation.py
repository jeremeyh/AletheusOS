from aletheus.constitutional_experience.constitutional_isolation.engine import Engine
from aletheus.constitutional_experience.models import ExperienceView


def test_founder_isolation():
    e = Engine()
    assert not e.authorize(
        ExperienceView.DEVELOPER, "platform_omniscience", True
    ).allowed
    assert e.authorize(ExperienceView.FOUNDER, "platform_omniscience", True).allowed
