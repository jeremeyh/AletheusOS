from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REGISTRY_DIR = ROOT / "aletheus/runtime/commands_v2"
REGISTRY_FILE = REGISTRY_DIR / "registry.py"
DISPATCHER_FILE = REGISTRY_DIR / "dispatcher.py"
TEST_FILE = ROOT / "aletheus/runtime/commands/tests/test_compiled_registry_dispatcher.py"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = (
    ROOT
    / "reports/genesis_8_command_dispatch"
    / f"backup_{timestamp}"
)
backup_dir.mkdir(parents=True, exist_ok=True)

if REGISTRY_FILE.exists():
    shutil.copy2(
        REGISTRY_FILE,
        backup_dir / "registry.py",
    )

if DISPATCHER_FILE.exists():
    shutil.copy2(
        DISPATCHER_FILE,
        backup_dir / "dispatcher.py",
    )

DISPATCHER_SOURCE = '''\
"""
AletheusOS Compiled Runtime Command Dispatcher

Genesis 8

The dispatcher receives an immutable command-table snapshot from
RuntimeCommandRegistry. It owns payload-command lookup, invocation,
normalization, and failure isolation.

Reflection and registration never occur in the hot dispatch path.
"""

from __future__ import annotations

from hashlib import sha256
from types import MappingProxyType
from typing import Any, Mapping

from .models import CommandRecord, CommandResult


class CompiledRuntimeCommandDispatcher:
    """
    Immutable payload-command execution index.

    A new dispatcher is compiled only when the registry changes.
    Normal command dispatch performs one mapping lookup.
    """

    __slots__ = (
        "_commands",
        "_fingerprint",
        "_generation",
    )

    def __init__(
        self,
        commands: Mapping[str, CommandRecord],
        *,
        generation: int = 0,
    ) -> None:
        snapshot = dict(commands)

        self._commands: Mapping[str, CommandRecord] = (
            MappingProxyType(snapshot)
        )
        self._generation = generation
        self._fingerprint = self._build_fingerprint(snapshot)

    @staticmethod
    def _build_fingerprint(
        commands: Mapping[str, CommandRecord],
    ) -> str:
        rows: list[str] = []

        for name in sorted(commands):
            record = commands[name]
            handler = record.handler

            rows.append(
                "|".join(
                    (
                        name,
                        str(record.category),
                        str(record.description),
                        getattr(handler, "__module__", ""),
                        getattr(handler, "__qualname__", repr(handler)),
                    )
                )
            )

        payload = "\\n".join(rows).encode("utf-8")
        return sha256(payload).hexdigest()

    @property
    def fingerprint(self) -> str:
        return self._fingerprint

    @property
    def generation(self) -> int:
        return self._generation

    @property
    def count(self) -> int:
        return len(self._commands)

    def has(self, name: str) -> bool:
        return name in self._commands

    def get(self, name: str) -> CommandRecord | None:
        return self._commands.get(name)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._commands))

    def dispatch(
        self,
        name: str,
        payload: dict[str, Any] | None = None,
    ) -> CommandResult:
        normalized_payload = payload or {}
        record = self._commands.get(name)

        if record is None:
            return CommandResult(
                command=name,
                status="missing",
                response={
                    "error": (
                        f"Command '{name}' is not registered."
                    )
                },
            )

        try:
            response = record.handler(normalized_payload)

            return CommandResult(
                command=name,
                status="completed",
                response=(
                    response
                    if isinstance(response, dict)
                    else {"result": response}
                ),
            )

        except Exception as exc:
            return CommandResult(
                command=name,
                status="failed",
                response={
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                },
            )

    def health(self) -> dict[str, Any]:
        return {
            "status": "online",
            "mode": "compiled",
            "commands": self.count,
            "generation": self.generation,
            "fingerprint": self.fingerprint,
            "command_names": list(self.names()),
        }


__all__ = [
    "CompiledRuntimeCommandDispatcher",
]
'''

REGISTRY_SOURCE = '''\
"""
AletheusOS Runtime Command Registry

Genesis 8 compiled-dispatch integration.

The public Genesis 7 registry contract remains stable while runtime
execution is delegated to an immutable compiled dispatcher.
"""

from __future__ import annotations

from typing import Any, Callable

from .dispatcher import CompiledRuntimeCommandDispatcher
from .models import CommandRecord, CommandResult


class RuntimeCommandRegistry:
    """
    Owns payload-command registration and compiled dispatch.

    Registration remains mutable for bootstrap compatibility. Every
    successful mutation recompiles an immutable dispatcher snapshot.
    Runtime command execution does not inspect or mutate the registry.
    """

    def __init__(self) -> None:
        self.commands: dict[str, CommandRecord] = {}
        self._generation = 0
        self._dispatcher = (
            CompiledRuntimeCommandDispatcher(
                self.commands,
                generation=self._generation,
            )
        )

    @property
    def dispatcher(self) -> CompiledRuntimeCommandDispatcher:
        return self._dispatcher

    @property
    def fingerprint(self) -> str:
        return self._dispatcher.fingerprint

    @property
    def generation(self) -> int:
        return self._generation

    def _compile(self) -> None:
        """
        Compile the mutable registration surface into an immutable
        runtime execution index.
        """

        self._generation += 1
        self._dispatcher = (
            CompiledRuntimeCommandDispatcher(
                self.commands,
                generation=self._generation,
            )
        )

    def register(
        self,
        name: str,
        handler: Callable[..., Any],
        category: str = "general",
        description: str = "",
        metadata: dict[str, Any] | None = None,
        *,
        replace: bool = False,
    ) -> CommandRecord:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Command name cannot be empty.")

        if normalized_name in self.commands:
            if not replace:
                # Genesis 7 idempotent-registration compatibility.
                return self.commands[normalized_name]

            self.commands.pop(normalized_name)

        record = CommandRecord(
            name=normalized_name,
            handler=handler,
            category=category,
            description=description,
            metadata=metadata or {},
        )

        self.commands[normalized_name] = record
        self._compile()

        return record

    def unregister(self, name: str) -> bool:
        removed = self.commands.pop(name, None) is not None

        if removed:
            self._compile()

        return removed

    def has(self, name: str) -> bool:
        return self._dispatcher.has(name)

    def get(self, name: str) -> CommandRecord | None:
        return self._dispatcher.get(name)

    def dispatch(
        self,
        name: str,
        payload: dict[str, Any] | None = None,
    ) -> CommandResult:
        return self._dispatcher.dispatch(name, payload)

    def count(self) -> int:
        return len(self.commands)

    def list(self) -> list[str]:
        return sorted(self.commands)

    def categories(self) -> list[str]:
        return sorted(
            {
                record.category
                for record in self.commands.values()
            }
        )

    def health(self) -> dict[str, Any]:
        return {
            "status": "online",
            "mode": "compiled",
            "commands": self.count(),
            "categories": self.categories(),
            "command_names": self.list(),
            "generation": self.generation,
            "fingerprint": self.fingerprint,
            "dispatcher": self._dispatcher.health(),
        }


__all__ = [
    "RuntimeCommandRegistry",
]
'''

TEST_SOURCE = '''\
from __future__ import annotations

from aletheus.runtime.commands_v2.registry import (
    RuntimeCommandRegistry,
)


def test_registry_dispatches_through_compiled_dispatcher():
    registry = RuntimeCommandRegistry()

    registry.register(
        "math.add",
        lambda payload: {
            "value": payload["left"] + payload["right"]
        },
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
'''

DISPATCHER_FILE.write_text(
    DISPATCHER_SOURCE,
    encoding="utf-8",
)
REGISTRY_FILE.write_text(
    REGISTRY_SOURCE,
    encoding="utf-8",
)

TEST_FILE.parent.mkdir(parents=True, exist_ok=True)
TEST_FILE.write_text(
    TEST_SOURCE,
    encoding="utf-8",
)

print("Genesis 8 compiled dispatcher installed.")
print(f"Backup:     {backup_dir.relative_to(ROOT)}")
print(f"Dispatcher: {DISPATCHER_FILE.relative_to(ROOT)}")
print(f"Registry:   {REGISTRY_FILE.relative_to(ROOT)}")
print(f"Tests:      {TEST_FILE.relative_to(ROOT)}")
