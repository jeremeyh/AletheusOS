"""
AletheusOS
Genesis 52.0

Constitutional Runtime™

Runtime Registry
"""

from __future__ import annotations

from .models import RuntimeContext


class RuntimeRegistry:
    """
    Registry of active and historical
    constitutional executions.

    The registry owns execution contexts.

    It never performs orchestration.
    """

    GENESIS = "52.0"
    VERSION = "1.0.0"

    def __init__(self) -> None:

        self._executions: dict[str, RuntimeContext] = {}

    #
    # Registration
    #

    def register(
        self,
        context: RuntimeContext,
    ) -> RuntimeContext:

        self._executions[
            context.execution_id
        ] = context

        return context

    #
    # Retrieval
    #

    def get(
        self,
        execution_id: str,
    ) -> RuntimeContext | None:

        return self._executions.get(
            execution_id
        )

    def all(self) -> list[RuntimeContext]:

        return sorted(
            self._executions.values(),
            key=lambda c: c.created_at,
        )

    #
    # Session Queries
    #

    def by_session(
        self,
        session_id: str,
    ) -> list[RuntimeContext]:

        return [

            context

            for context in self._executions.values()

            if context.session_id == session_id

        ]

    #
    # Lifecycle
    #

    def remove(
        self,
        execution_id: str,
    ) -> None:

        self._executions.pop(
            execution_id,
            None,
        )

    #
    # Diagnostics
    #

    def health(self) -> dict:

        return {

            "name": "Runtime Registry",

            "genesis": self.GENESIS,

            "version": self.VERSION,

            "status": "healthy",

            "registered_executions": len(
                self._executions
            ),
        }

    def statistics(self) -> dict:

        statuses: dict[str, int] = {}

        for context in self._executions.values():

            statuses.setdefault(
                context.status.value,
                0,
            )

            statuses[
                context.status.value
            ] += 1

        return {

            "name": "Runtime Registry",

            "genesis": self.GENESIS,

            "version": self.VERSION,

            "registered_executions": len(
                self._executions
            ),

            "statuses": statuses,
        }


runtime_registry = RuntimeRegistry()
