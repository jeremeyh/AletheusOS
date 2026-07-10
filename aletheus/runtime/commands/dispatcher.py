from __future__ import annotations

import inspect
from typing import Any, Awaitable, Callable, Iterable

from .contracts import CommandContext, CommandMiddleware, NextHandler
from .errors import (
    CommandDispatchError,
    CommandExecutionError,
    CommandResultTypeError,
    CommandValidationError,
)
from .models import CompiledCommand
from .registry import CompiledCommandRegistry


class CommandDispatcher:
    """
    Canonical governed command execution path.

    Runtime flow:
      lookup -> request validation -> global middleware ->
      command middleware -> handler -> result validation
    """

    __slots__ = ("_registry", "_middleware", "_wrap_unhandled")

    def __init__(
        self,
        registry: CompiledCommandRegistry,
        middleware: Iterable[CommandMiddleware] = (),
        *,
        wrap_unhandled_exceptions: bool = True,
    ) -> None:
        self._registry = registry
        self._middleware = tuple(middleware)
        self._wrap_unhandled = wrap_unhandled_exceptions

    @property
    def registry(self) -> CompiledCommandRegistry:
        return self._registry

    async def dispatch(
        self,
        command_name: str,
        request: Any,
        *,
        context: CommandContext | None = None,
    ) -> Any:
        command = self._registry.require(command_name)
        active_context = context or CommandContext()

        self._validate_request(command, request)

        terminal = self._terminal(command)
        pipeline = self._compose(
            (*self._middleware, *command.middleware),
            terminal,
        )

        try:
            result = await pipeline(active_context, request)
            self._validate_result(command, result)
            return result
        except CommandDispatchError:
            raise
        except BaseException as exc:
            if not self._wrap_unhandled:
                raise
            raise CommandExecutionError(command.name, exc) from exc

    @staticmethod
    def _validate_request(command: CompiledCommand, request: Any) -> None:
        if not isinstance(request, command.request_type):
            raise CommandValidationError(
                command.name,
                (
                    f"expected {command.request_type.__qualname__}, "
                    f"got {type(request).__qualname__}"
                ),
            )

    @staticmethod
    def _validate_result(command: CompiledCommand, result: Any) -> None:
        if not isinstance(result, command.result_type):
            raise CommandResultTypeError(
                command.name,
                command.result_type,
                type(result),
            )

    @staticmethod
    def _terminal(command: CompiledCommand) -> NextHandler:
        async def invoke(context: CommandContext, request: Any) -> Any:
            value = command.handler(context, request)
            if inspect.isawaitable(value):
                return await value
            return value

        return invoke

    @staticmethod
    def _compose(
        middleware: tuple[CommandMiddleware, ...],
        terminal: NextHandler,
    ) -> NextHandler:
        pipeline = terminal

        for component in reversed(middleware):
            next_handler = pipeline

            async def invoke(
                context: CommandContext,
                request: Any,
                *,
                _component: CommandMiddleware = component,
                _next: NextHandler = next_handler,
            ) -> Any:
                value = _component(context, request, _next)
                if inspect.isawaitable(value):
                    return await value
                return value

            pipeline = invoke

        return pipeline
