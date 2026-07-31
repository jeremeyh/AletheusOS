from aletheus.tooling.kinekt.resolution.policy import ResolutionPolicy
from aletheus.tooling.kinekt.resolution.scoring import resolve_finding


def test_syntax_error_is_critical() -> None:
    item = resolve_finding(
        {
            "code": "SYNTAX_ERROR",
            "subject": "aletheus.bad",
            "evidence": ["aletheus/bad.py"],
        },
        ResolutionPolicy(),
    )

    assert item.tier == "critical"
    assert item.disposition == "repair"


def test_archived_duplicate_is_suppressed() -> None:
    item = resolve_finding(
        {
            "code": "EXACT_STRUCTURAL_DUPLICATE",
            "subject": "archive.old",
            "evidence": [
                "archive/old.py",
                "backups/old.py",
            ],
        },
        ResolutionPolicy(),
    )

    assert item.tier == "suppressed"
