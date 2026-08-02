from aletheus.card_hawk_navigation.workspace_composer.engine import Engine
from aletheus.card_hawk_navigation.workspace_composer.models import (
    WorkspacePriority,
    WorkspaceRegion,
)


def test_compose():
    assert (
        Engine().compose(
            (WorkspaceRegion("f", "field_vision", WorkspacePriority.PRIMARY),)
        )["valid"]
        is True
    )
