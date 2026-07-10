from dataclasses import dataclass

import pytest

from aletheus.runtime.commands import (
    CommandContext,
    CommandDispatcher,
    CommandNotFoundError,
    CommandResultTypeError,
    CommandValidationError,
    CompiledCommand,
    CompiledCommandRegistry,
    DuplicateCommandError,
)


@dataclass(frozen=True, slots=True)
class AddRequest:
    left: int
    right: int


@dataclass(frozen=True, slots=True)
class AddResult:
    value: int


async def add_handler(
    context: CommandContext,
    request: AddRequest,
) -> AddResult:
    return AddResult(request.left + request.right)


class TraceMiddleware:
    def __init__(self, events: list[str], name: str) -> None:
        self.events = events
        self.name = name

    async def __call__(self, context, request, call_next):
        self.events.append(f"{self.name}:before")
        result = await call_next(context, request)
        self.events.append(f"{self.name}:after")
        return result


def build_command(*, middleware=()):
    return CompiledCommand(
        name="math.add",
        domain="math",
        version="1",
        handler=add_handler,
        request_type=AddRequest,
        result_type=AddResult,
        middleware=tuple(middleware),
        aliases=("math.sum",),
        idempotent=True,
    )


@pytest.mark.asyncio
async def test_dispatches_registered_command():
    dispatcher = CommandDispatcher(
        CompiledCommandRegistry([build_command()])
    )

    result = await dispatcher.dispatch("math.add", AddRequest(2, 3))

    assert result == AddResult(5)


@pytest.mark.asyncio
async def test_alias_uses_same_compiled_command():
    dispatcher = CommandDispatcher(
        CompiledCommandRegistry([build_command()])
    )

    result = await dispatcher.dispatch("math.sum", AddRequest(4, 6))

    assert result == AddResult(10)


@pytest.mark.asyncio
async def test_global_middleware_wraps_command_middleware():
    events: list[str] = []
    command = build_command(
        middleware=(TraceMiddleware(events, "command"),)
    )
    dispatcher = CommandDispatcher(
        CompiledCommandRegistry([command]),
        middleware=(TraceMiddleware(events, "global"),),
    )

    await dispatcher.dispatch("math.add", AddRequest(1, 1))

    assert events == [
        "global:before",
        "command:before",
        "command:after",
        "global:after",
    ]


@pytest.mark.asyncio
async def test_rejects_invalid_request_type():
    dispatcher = CommandDispatcher(
        CompiledCommandRegistry([build_command()])
    )

    with pytest.raises(CommandValidationError):
        await dispatcher.dispatch("math.add", object())


@pytest.mark.asyncio
async def test_rejects_invalid_result_type():
    async def bad_handler(context, request):
        return "invalid"

    command = CompiledCommand(
        name="math.bad",
        domain="math",
        version="1",
        handler=bad_handler,
        request_type=AddRequest,
        result_type=AddResult,
    )
    dispatcher = CommandDispatcher(CompiledCommandRegistry([command]))

    with pytest.raises(CommandResultTypeError):
        await dispatcher.dispatch("math.bad", AddRequest(1, 2))


@pytest.mark.asyncio
async def test_missing_command_fails_cleanly():
    dispatcher = CommandDispatcher(CompiledCommandRegistry([]))

    with pytest.raises(CommandNotFoundError):
        await dispatcher.dispatch("missing.command", AddRequest(1, 2))


def test_duplicate_alias_or_command_is_rejected():
    first = build_command()
    second = CompiledCommand(
        name="math.other",
        domain="math",
        version="1",
        handler=add_handler,
        request_type=AddRequest,
        result_type=AddResult,
        aliases=("math.sum",),
    )

    with pytest.raises(DuplicateCommandError):
        CompiledCommandRegistry([first, second])


def test_registry_fingerprint_is_deterministic():
    one = CompiledCommandRegistry([build_command()])
    two = CompiledCommandRegistry([build_command()])

    assert one.fingerprint == two.fingerprint
