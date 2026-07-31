from aletheus.concept_collision_engine import (
    ConceptCollisionService,
    ConceptSignature,
)


def test_exact_name_collision_fails():
    service = ConceptCollisionService()
    service.register_concept(ConceptSignature(name="Atlas™", owns="Architecture"))

    report = service.evaluate(ConceptSignature(name="Atlas™", owns="Architecture"))

    assert report.passed is False
    assert report.findings


def test_unique_concept_passes():
    service = ConceptCollisionService()
    service.register_concept(ConceptSignature(name="Atlas™", owns="Architecture"))

    report = service.evaluate(
        ConceptSignature(name="New Unique Concept", owns="Unique Domain")
    )

    assert report.passed is True
