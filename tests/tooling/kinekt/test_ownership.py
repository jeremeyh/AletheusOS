from pathlib import PurePosixPath

from aletheus.tooling.kinekt.ownership import infer_owner


def test_runtime_owner() -> None:
    assert (
        infer_owner(PurePosixPath("aletheus/runtime/core.py"))
        == "Constitutional Runtime Kernel"
    )
