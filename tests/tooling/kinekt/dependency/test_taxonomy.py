from aletheus.tooling.kinekt.dependency.taxonomy import infer_capability


def test_runtime_capability() -> None:
    assert (
        infer_capability("aletheus.runtime.core", "Constitutional Runtime Kernel")
        == "Constitutional Runtime Kernel"
    )


def test_unknown_capability() -> None:
    assert infer_capability("unknown.module", None) is None
