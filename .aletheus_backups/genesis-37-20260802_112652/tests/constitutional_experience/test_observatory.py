import pytest

from aletheus.constitutional_experience.founder_observatory.engine import Engine
from aletheus.constitutional_experience.models import ExperienceView


def test_denied():
    with pytest.raises(PermissionError):
        Engine().summarize([], view=ExperienceView.ADMIN, root_attested=True)


def test_founder():
    r = Engine().summarize(
        [{"actor_type": "developer", "action": "patch"}],
        view=ExperienceView.FOUNDER,
        root_attested=True,
    )
    assert r["visibility"] == "ecosystem-totality"
