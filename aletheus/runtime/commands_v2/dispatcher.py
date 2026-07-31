"""
AletheusOS Compiled Runtime Command Dispatcher

Genesis 8

Handler signatures are classified once when the immutable dispatcher is
compiled. Runtime dispatch performs no reflection.
"""

from __future__ import annotations

import inspect
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from types import MappingProxyType
from typing import Any, Literal

from aletheus.runtime.context import RuntimeContext

from .models import CommandRecord, CommandResult

InvocationMode = Literal[
    "context",
    "payload",
    "no_arguments",
]


@dataclass(frozen=True, slots=True)
class CompiledCommandEntry:
    record: CommandRecord
    invocation_mode: InvocationMode
    result_key: str | None = None


class CompiledRuntimeCommandDispatcher:
    """
    Immutable payload-command execution index.

    Handler invocation modes and legacy response-envelope contracts are
    resolved during compilation rather than during normal dispatch.
    """

    RESULT_KEY_CONTRACTS: dict[str, str] = {
        "plugin.bootstrap": "plugin",
        "plugin.install": "plugin",
        "plugin.enable": "plugin",
        "plugin.disable": "plugin",
        "plugin.remove": "plugin",
        "plugin.statistics": "plugin_stats",
        "kernel.bootstrap": "kernel",
        "kernel.boot": "kernel",
        "kernel.sync": "kernel",
        "kernel.publish": "event",
        "kernel.snapshot": "snapshot",
        "kernel.execute": "task",
        "kernel.tasks": "tasks",
        "kernel.scheduler": "schedule",
        "kernel.dispatcher": "dispatch",
        "kernel.supervisor": "supervisor",
        "kernel.statistics": "kernel_stats",
        "state.bootstrap": "state",
        "state.save": "state",
        "state.load": "state",
        "state.snapshot": "snapshot",
        "state.restore": "state",
        "state.export": "state",
        "state.import": "state",
        "state.statistics": "state_stats",
        "federation.bootstrap": "federation",
        "federation.join": "node",
        "federation.discover": "nodes",
        "federation.query": "federation",
        "federation.broadcast": "broadcast",
        "federation.leave": "node",
        "federation.statistics": "federation_stats",
        "telemetry.bootstrap": "telemetry",
        "telemetry.metric": "metric",
        "telemetry.record": "record",
        "telemetry.log": "log",
        "telemetry.trace": "trace",
        "telemetry.health": "health",
        "telemetry.timeline": "timeline",
        "telemetry.statistics": "telemetry_stats",
        "ha.bootstrap": "ha",
        "ha.join": "node",
        "ha.status": "ha_status",
        "ha.replicate": "replication",
        "ha.failover": "failover",
        "ha.statistics": "ha_stats",
        "security.bootstrap": "security",
        "security.authenticate": "authentication",
        "security.authorize": "authorization",
        "security.policy": "policy",
        "security.audit": "audit",
        "security.statistics": "security_stats",
        "security.role_create": "role",
        "security.role_assign": "assignment",
        "security.role.create": "role",
        "security.role.assign": "assignment",
        "tenant.bootstrap": "tenant",
        "organization.create": "organization",
        "tenant.create": "tenant",
        "workspace.create": "workspace",
        "tenant.statistics": "tenant_stats",
        "tenant.health": "tenant_health",
        "cluster.elect_leader": "leader",
        "mission.v2.create": "mission",
        "mission.v2.plan": "planning",
        "mission.v2.execute": "execution",
        "mission.v2.execute_next": "execution",
        "mission.v2.telemetry": "telemetry",
        "mission.v2.stats": "mission_v2_stats",
        "workflow.v2.create": "workflow",
        "workflow.v2.execute": "execution",
        "workflow.v2.execute_next": "execution",
        "workflow.v2.history": "history",
        "workflow.v2.stats": "workflow_v2_stats",
        "workspace.overview": "workspace",
        "workspace.stats": "workspace_stats",
        "founder.journal.create": "journal_entry",
        "founder.journal.list": "journal",
        "objective.create": "objective",
        "objective.list": "objectives",
        "notification.create": "notification",
        "notification.list": "notifications",
        "application.register": "application",
        "application.list": "applications",
        "application.start": "application",
        "application.stop": "application",
        "application.restart": "application",
        "application.health": "application_health",
        "application.stats": "application_stats",
        "application.install": "application",
        "application.uninstall": "application",
        "application.manifest": "manifest",
        "application.events": "events",
        "application.bootstrap.defaults": "applications",
        "cardhawk.start": "cardhawk",
        "cardhawk.status": "cardhawk",
        "semantic.concept.create": "concept",
        "semantic.concept.search": "concepts",
        "semantic.assert": "assertion",
        "semantic.query": "assertions",
        "semantic.explain": "explanation",
        "semantic.bootstrap.cardhawk": "bootstrap",
        "semantic.stats": "semantic_stats",
        "executive.status": "executive_status",
        "executive.snapshot": "snapshot",
        "executive.summary": "summary",
        "executive.recommendations": "recommendations",
        "executive.risks": "risks",
        "executive.daily_brief": "brief",
        "executive.system_report": "system_report",
        "uil.context": "context",
        "uil.reason": "reasoning",
        "uil.synthesize": "synthesis",
        "uil.decide": "decision",
        "uil.brief": "brief",
        "uil.snapshot": "snapshot",
        "uil.timeline": "timeline",
        "uil.stats": "uil_stats",
        "goal.create": "goal",
        "goal.complete": "goal",
        "goal.list": "goals",
        "plan.generate": "plan",
        "plan.list": "plans",
        "reason.evaluate": "reasoning",
        "decision.record": "decision",
        "decision.history": "decisions",
        "planning.create": "plan",
        "planning.execute_next": "execution",
        "planning.execute": "execution",
        "planning.statistics": "planning_stats",
        "plan.bootstrap": "planning",
        "plan.create": "plan",
        "plan.execute": "plan",
        "plan.progress": "plan",
        "plan.replan": "plan",
        "plan.complete": "plan",
        "plan.statistics": "planning_stats",
        "cluster.bootstrap": "cluster",
        "cluster.join": "node",
        "cluster.nodes": "nodes",
        "cluster.heartbeat": "heartbeat",
        "node.heartbeat": "heartbeat",
        "cluster.status": "cluster_status",
        "cluster.statistics": "cluster_stats",
        "cluster.stats": "cluster_stats",
        "cluster.broadcast": "broadcast",
        "cluster.task.assign": "task",
        "compat.statistics": "compat_stats",
        "agent.task.assign": "task",
        "agent.run": "agent_run",
        "agent.orchestrate": "orchestration",
    }

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
        compiled = {
            name: CompiledCommandEntry(
                record=record,
                invocation_mode=self._classify_handler(record.handler),
                result_key=(
                    record.metadata.get("result_key")
                    or self.RESULT_KEY_CONTRACTS.get(name)
                ),
            )
            for name, record in commands.items()
        }

        self._commands: Mapping[
            str,
            CompiledCommandEntry,
        ] = MappingProxyType(compiled)

        self._generation = generation
        self._fingerprint = self._build_fingerprint(compiled)

    @staticmethod
    def _classify_handler(
        handler: Any,
    ) -> InvocationMode:
        """
        Classify a handler once at registry compilation.

        Context classification uses both the first parameter name and its
        annotation so older unannotated handlers remain compatible.
        """

        try:
            signature = inspect.signature(handler)
        except (TypeError, ValueError):
            return "payload"

        parameters = list(signature.parameters.values())

        positional = [
            parameter
            for parameter in parameters
            if parameter.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]

        if not positional:
            return "no_arguments"

        first = positional[0]
        annotation = first.annotation

        annotation_name = ""

        if annotation is not inspect.Signature.empty:
            annotation_name = getattr(
                annotation,
                "__name__",
                str(annotation),
            )

        normalized_name = first.name.lower()

        if (
            normalized_name
            in {
                "context",
                "ctx",
                "runtime_context",
                "command_context",
            }
            or "RuntimeContext" in annotation_name
        ):
            return "context"

        return "payload"

    @staticmethod
    def _handler_identity(handler: Any) -> str:
        code = getattr(handler, "__code__", None)

        if code is None:
            return "|".join(
                (
                    getattr(handler, "__module__", ""),
                    getattr(
                        handler,
                        "__qualname__",
                        repr(handler),
                    ),
                    type(handler).__module__,
                    type(handler).__qualname__,
                )
            )

        closure = getattr(handler, "__closure__", None) or ()

        closure_values = tuple(repr(cell.cell_contents) for cell in closure)

        return repr(
            (
                getattr(handler, "__module__", ""),
                getattr(handler, "__qualname__", ""),
                code.co_code,
                code.co_consts,
                code.co_names,
                code.co_varnames,
                getattr(handler, "__defaults__", None),
                getattr(handler, "__kwdefaults__", None),
                closure_values,
            )
        )

    @classmethod
    def _build_fingerprint(
        cls,
        commands: Mapping[str, CompiledCommandEntry],
    ) -> str:
        rows: list[str] = []

        for name in sorted(commands):
            entry = commands[name]
            record = entry.record

            rows.append(
                "|".join(
                    (
                        name,
                        str(record.category),
                        str(record.description),
                        repr(record.metadata),
                        entry.invocation_mode,
                        str(entry.result_key),
                        cls._handler_identity(record.handler),
                    )
                )
            )

        payload = "\n".join(rows).encode("utf-8")
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
        entry = self._commands.get(name)

        if entry is None:
            return None

        return entry.record

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._commands))

    def invocation_mode(
        self,
        name: str,
    ) -> InvocationMode | None:
        entry = self._commands.get(name)

        if entry is None:
            return None

        return entry.invocation_mode

    @staticmethod
    def _invoke(
        entry: CompiledCommandEntry,
        *,
        name: str,
        payload: dict[str, Any],
        application: str,
    ) -> Any:
        handler = entry.record.handler

        if entry.invocation_mode == "no_arguments":
            return handler()

        if entry.invocation_mode == "context":
            context = RuntimeContext(
                command=name,
                payload=payload,
                application=application,
            )

            result = handler(context)

            # A mutating context handler may return None.
            return context if result is None else result

        return handler(payload)

    def dispatch(
        self,
        name: str,
        payload: dict[str, Any] | None = None,
        *,
        application: str = "system",
    ) -> CommandResult:
        normalized_payload = payload or {}
        entry = self._commands.get(name)

        if entry is None:
            return CommandResult(
                command=name,
                status="missing",
                response={"error": (f"Command '{name}' is not registered.")},
            )

        try:
            response = self._invoke(
                entry,
                name=name,
                payload=normalized_payload,
                application=application,
            )

            if isinstance(response, RuntimeContext):
                normalized_response = response

            elif entry.result_key is not None:
                normalized_response = {
                    entry.result_key: response,
                }

            elif isinstance(response, dict):
                normalized_response = response

            else:
                normalized_response = {
                    "result": response,
                }

            return CommandResult(
                command=name,
                status="completed",
                response=normalized_response,
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
        mode_counts = {
            "context": 0,
            "payload": 0,
            "no_arguments": 0,
        }

        for entry in self._commands.values():
            mode_counts[entry.invocation_mode] += 1

        return {
            "status": "online",
            "mode": "compiled",
            "commands": self.count,
            "generation": self.generation,
            "fingerprint": self.fingerprint,
            "command_names": list(self.names()),
            "invocation_modes": mode_counts,
        }


__all__ = [
    "CompiledCommandEntry",
    "CompiledRuntimeCommandDispatcher",
    "InvocationMode",
]
