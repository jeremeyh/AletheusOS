from __future__ import annotations

from aletheus.runtime.commands_v2.registry import (
    RuntimeCommandRegistry,
)


def test_registry_dispatches_through_compiled_dispatcher():
    registry = RuntimeCommandRegistry()

    registry.register(
        "math.add",
        lambda payload: {"value": payload["left"] + payload["right"]},
        category="test",
    )

    result = registry.dispatch(
        "math.add",
        {
            "left": 2,
            "right": 3,
        },
    )

    assert result.status == "completed"
    assert result.response == {"value": 5}
    assert registry.health()["mode"] == "compiled"


def test_dispatcher_recompiles_after_registration():
    registry = RuntimeCommandRegistry()

    initial_generation = registry.generation
    initial_fingerprint = registry.fingerprint

    registry.register(
        "test.one",
        lambda payload: {"ok": True},
    )

    assert registry.generation == initial_generation + 1
    assert registry.fingerprint != initial_fingerprint
    assert registry.dispatcher.has("test.one")


def test_duplicate_registration_remains_idempotent():
    registry = RuntimeCommandRegistry()

    original = registry.register(
        "test.command",
        lambda payload: {"version": 1},
    )
    generation = registry.generation
    fingerprint = registry.fingerprint

    duplicate = registry.register(
        "test.command",
        lambda payload: {"version": 2},
    )

    result = registry.dispatch("test.command", {})

    assert duplicate is original
    assert registry.generation == generation
    assert registry.fingerprint == fingerprint
    assert result.response == {"version": 1}


def test_replace_registration_recompiles_dispatcher():
    registry = RuntimeCommandRegistry()

    registry.register(
        "test.command",
        lambda payload: {"version": 1},
    )
    generation = registry.generation
    fingerprint = registry.fingerprint

    registry.register(
        "test.command",
        lambda payload: {"version": 2},
        replace=True,
    )

    result = registry.dispatch("test.command", {})

    assert registry.generation == generation + 1
    assert registry.fingerprint != fingerprint
    assert result.response == {"version": 2}


def test_unregister_recompiles_and_removes_command():
    registry = RuntimeCommandRegistry()

    registry.register(
        "test.command",
        lambda payload: {"ok": True},
    )
    generation = registry.generation

    removed = registry.unregister("test.command")
    result = registry.dispatch("test.command", {})

    assert removed is True
    assert registry.generation == generation + 1
    assert result.status == "missing"


def test_missing_command_preserves_legacy_result_contract():
    registry = RuntimeCommandRegistry()

    result = registry.dispatch("missing.command", {})

    assert result.command == "missing.command"
    assert result.status == "missing"
    assert "not registered" in result.response["error"]


def test_handler_failure_preserves_legacy_result_contract():
    registry = RuntimeCommandRegistry()

    def fail(payload):
        raise RuntimeError("controlled failure")

    registry.register("test.fail", fail)

    result = registry.dispatch("test.fail", {})

    assert result.command == "test.fail"
    assert result.status == "failed"
    assert result.response["error"] == "controlled failure"
    assert result.response["error_type"] == "RuntimeError"


def test_non_dictionary_response_is_normalized():
    registry = RuntimeCommandRegistry()

    registry.register(
        "test.scalar",
        lambda payload: 42,
    )

    result = registry.dispatch("test.scalar", {})

    assert result.status == "completed"
    assert result.response == {"result": 42}


def test_compiled_dispatcher_snapshot_is_immutable():
    registry = RuntimeCommandRegistry()

    registry.register(
        "test.one",
        lambda payload: {"one": True},
    )

    first_dispatcher = registry.dispatcher

    registry.register(
        "test.two",
        lambda payload: {"two": True},
    )

    assert first_dispatcher.has("test.one")
    assert not first_dispatcher.has("test.two")
    assert registry.dispatcher.has("test.two")


def test_health_exposes_generation_and_fingerprint():
    registry = RuntimeCommandRegistry()

    registry.register(
        "test.health",
        lambda payload: {"ok": True},
        category="health",
    )

    health = registry.health()

    assert health["mode"] == "compiled"
    assert health["generation"] == registry.generation
    assert health["fingerprint"] == registry.fingerprint
    assert len(health["fingerprint"]) == 64
    assert health["dispatcher"]["mode"] == "compiled"
