from aletheus.tooling.kinekt.integrity.scoring import (
    score_repository,
    score_resolution,
)


def test_repository_scoring() -> None:
    dimensions = score_repository(
        {
            "findings": [
                {"code": "BOUNDARY_VIOLATION"},
                {"code": "ORPHAN_CANDIDATE"},
            ]
        }
    )

    by_name = {dimension.name: dimension for dimension in dimensions}
    assert by_name["boundaries"].score == 90
    assert by_name["reachability"].score == 99.75


def test_resolution_scoring() -> None:
    dimension = score_resolution(
        {
            "items": [
                {"tier": "high"},
                {"tier": "medium"},
            ]
        }
    )

    assert dimension.score == 91
