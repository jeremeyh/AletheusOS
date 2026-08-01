from aletheus.nimble.composer.engine import Engine, ExperienceNode
from aletheus.nimble.composer.models import PrimitiveDefinition


def test_composer() -> None:
    catalog = (
        PrimitiveDefinition("Surface", "structure", "surface"),
        PrimitiveDefinition("Heading", "typography", "heading"),
    )
    report = Engine().compose(
        ExperienceNode("Surface", (ExperienceNode("Heading"),)), catalog
    )
    assert report["valid"] and report["node_count"] == 2
