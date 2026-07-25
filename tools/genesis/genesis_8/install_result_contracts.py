from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DISPATCHER = ROOT / "aletheus/runtime/commands_v2/dispatcher.py"
COMMAND_BUS = ROOT / "aletheus/runtime/commands/command_bus.py"

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = (
    ROOT
    / "reports/genesis_8_command_dispatch"
    / f"result_contract_backup_{stamp}"
)
backup.mkdir(parents=True, exist_ok=True)

shutil.copy2(DISPATCHER, backup / "dispatcher.py")
shutil.copy2(COMMAND_BUS, backup / "command_bus.py")


dispatcher_text = DISPATCHER.read_text(encoding="utf-8")

old_entry = '''\
@dataclass(frozen=True, slots=True)
class CompiledCommandEntry:
    record: CommandRecord
    invocation_mode: InvocationMode
'''

new_entry = '''\
@dataclass(frozen=True, slots=True)
class CompiledCommandEntry:
    record: CommandRecord
    invocation_mode: InvocationMode
    result_key: str | None = None
'''

if old_entry not in dispatcher_text:
    raise RuntimeError("CompiledCommandEntry block not found.")

dispatcher_text = dispatcher_text.replace(old_entry, new_entry)


old_class_start = '''\
class CompiledRuntimeCommandDispatcher:
    """
    Immutable payload-command execution index.

    Handler invocation modes are resolved during compilation rather than
    during normal dispatch.
    """
'''

new_class_start = '''\
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

        "tenant.bootstrap": "tenant",
        "organization.create": "organization",
        "tenant.create": "tenant",
        "workspace.create": "workspace",
        "tenant.statistics": "tenant_stats",
        "tenant.health": "tenant_health",

        "cluster.join": "node",
        "cluster.elect_leader": "leader",
        "cluster.heartbeat": "heartbeat",
    }
'''

if old_class_start not in dispatcher_text:
    raise RuntimeError("Dispatcher class header not found.")

dispatcher_text = dispatcher_text.replace(
    old_class_start,
    new_class_start,
)


old_compilation = '''\
        compiled = {
            name: CompiledCommandEntry(
                record=record,
                invocation_mode=self._classify_handler(
                    record.handler
                ),
            )
            for name, record in commands.items()
        }
'''

new_compilation = '''\
        compiled = {
            name: CompiledCommandEntry(
                record=record,
                invocation_mode=self._classify_handler(
                    record.handler
                ),
                result_key=(
                    record.metadata.get("result_key")
                    or self.RESULT_KEY_CONTRACTS.get(name)
                ),
            )
            for name, record in commands.items()
        }
'''

if old_compilation not in dispatcher_text:
    raise RuntimeError("Dispatcher compilation block not found.")

dispatcher_text = dispatcher_text.replace(
    old_compilation,
    new_compilation,
)


old_fingerprint_row = '''\
                        repr(record.metadata),
                        entry.invocation_mode,
                        cls._handler_identity(record.handler),
'''

new_fingerprint_row = '''\
                        repr(record.metadata),
                        entry.invocation_mode,
                        str(entry.result_key),
                        cls._handler_identity(record.handler),
'''

if old_fingerprint_row not in dispatcher_text:
    raise RuntimeError("Fingerprint row block not found.")

dispatcher_text = dispatcher_text.replace(
    old_fingerprint_row,
    new_fingerprint_row,
)


old_response = '''\
            return CommandResult(
                command=name,
                status="completed",
                response=response,
            )
'''

new_response = '''\
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
'''

if old_response not in dispatcher_text:
    # Accommodate the scalar-normalization patch if already applied.
    old_response = '''\
            return CommandResult(
                command=name,
                status="completed",
                response=(
                    response
                    if isinstance(
                        response,
                        (dict, RuntimeContext),
                    )
                    else {"result": response}
                ),
            )
'''

if old_response not in dispatcher_text:
    raise RuntimeError("Completed response block not found.")

dispatcher_text = dispatcher_text.replace(
    old_response,
    new_response,
    1,
)

DISPATCHER.write_text(
    dispatcher_text,
    encoding="utf-8",
)

print("Genesis 8 compiled result contracts installed.")
print(f"Backup: {backup.relative_to(ROOT)}")
print(f"Updated: {DISPATCHER.relative_to(ROOT)}")
