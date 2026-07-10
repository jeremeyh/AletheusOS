from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Protocol

from .contracts import CommandContext, NextHandler
from .errors import CommandValidationError


class Authorizer(Protocol):
    async def authorize(
        self,
        context: CommandContext,
        command_name: str,
        permissions: tuple[str, ...],
    ) -> None:
        ...


@dataclass(slots=True)
class TimingMiddleware:
    observe: Callable[[str, float, bool], None]
    command_name: str

    async def __call__(
        self,
        context: CommandContext,
        request: Any,
        call_next: NextHandler,
    ) -> Any:
        started = time.perf_counter()
        succeeded = False
        try:
            result = await call_next(context, request)
            succeeded = True
            return result
        finally:
            self.observe(self.command_name, time.perf_counter() - started, succeeded)


@dataclass(slots=True)
class AuthorizationMiddleware:
    authorizer: Authorizer
    command_name: str
    permissions: tuple[str, ...]

    async def __call__(
        self,
        context: CommandContext,
        request: Any,
        call_next: NextHandler,
    ) -> Any:
        await self.authorizer.authorize(
            context,
            self.command_name,
            self.permissions,
        )
        return await call_next(context, request)


@dataclass(slots=True)
class PredicateMiddleware:
    command_name: str
    predicate: Callable[[CommandContext, Any], bool]
    message: str

    async def __call__(
        self,
        context: CommandContext,
        request: Any,
        call_next: NextHandler,
    ) -> Any:
        if not self.predicate(context, request):
            raise CommandValidationError(self.command_name, self.message)
        return await call_next(context, request)
