from aletheus.constitutional_experience.spatial_physics.engine import Engine, Spring


def test_spring():
    s = Spring(target=1)
    Engine().step(s, 0.016)
    assert 0 < s.position < 1
