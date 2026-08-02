from pathlib import Path

from aletheus.constitutional_experience.production_distribution.engine import (
    ExperienceDistributionEngine,
)


def test_canonical_plan_is_valid():
    plan = ExperienceDistributionEngine().canonical_plan()
    assert plan.validate() == []


def test_founder_observatory_is_restricted():
    plan = ExperienceDistributionEngine().canonical_plan()
    founder = next(
        artifact
        for artifact in plan.artifacts
        if artifact.artifact_id == "founder_observatory"
    )
    assert founder.founder_restricted is True


def test_required_roots(tmp_path: Path):
    engine = ExperienceDistributionEngine()
    for root in engine.REQUIRED_ROOTS:
        (tmp_path / root).mkdir()
    assert engine.validate_distribution_root(tmp_path) == []


def test_plan_writes(tmp_path: Path):
    target = tmp_path / "plan.json"
    ExperienceDistributionEngine().write_plan(target)
    assert target.exists()
    assert "AletheusOS-Genesis37-CoreUI" in target.read_text()
