import json

from aletheus.tooling.runtime_dependency_injection.container import DependencyContainer
from aletheus.tooling.runtime_dependency_injection.engine import InjectionEngine


def test_container_resolves_singleton() -> None:
    container = DependencyContainer()
    container.register("x", lambda _: object())
    assert container.resolve("x") is container.resolve("x")


def test_injection_builds_bindings(tmp_path) -> None:
    registry = tmp_path / "registry.json"
    authority = tmp_path / "authority.json"
    registry.write_text(json.dumps({"engines": [{"engine_name": "A"}]}))
    authority.write_text(json.dumps({"capabilities": [{"name": "A"}]}))
    report = InjectionEngine(registry, authority, tmp_path / "out").build()
    assert report["binding_count"] == 1
