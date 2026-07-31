from aletheus.tooling.kinekt.graph import RepositoryGraph
from aletheus.tooling.kinekt.models import ModuleRecord


def _module(name: str, imports: tuple[str, ...] = ()) -> ModuleRecord:
    return ModuleRecord(
        module=name,
        path=f"{name.replace('.', '/')}.py",
        package=name.split(".")[0],
        owner="test",
        lines=1,
        imports=imports,
        definitions=(),
    )


def test_graph_resolves_internal_imports() -> None:
    graph = RepositoryGraph(
        [
            _module("aletheus.alpha", ("aletheus.beta",)),
            _module("aletheus.beta"),
        ]
    )

    assert graph.fan_out("aletheus.alpha") == 1
    assert graph.fan_in("aletheus.beta") == 1
