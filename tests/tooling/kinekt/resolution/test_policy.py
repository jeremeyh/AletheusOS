from aletheus.tooling.kinekt.resolution.policy import ResolutionPolicy


def test_generated_reports_are_suppressed() -> None:
    policy = ResolutionPolicy()
    assert policy.path_is_suppressed(
        "reports/architecture/kinekt/repository-intelligence.json"
    )


def test_canonical_source_is_not_suppressed() -> None:
    policy = ResolutionPolicy()
    assert not policy.path_is_suppressed("aletheus/runtime/core.py")
