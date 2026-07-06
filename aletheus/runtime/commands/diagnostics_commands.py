from __future__ import annotations

from typing import Any

from aletheus.runtime.context import RuntimeContext


def register_diagnostics_commands(runtime: Any) -> None:
    """
    Register diagnostics and observability commands with the runtime command bus.

    This module is part of Genesis 6 core decomposition. It removes
    health, status, metrics, audit, boot, and platform-observation
    handlers from runtime/core.py while preserving runtime behavior.
    """
    runtime.commands.register("cognition.stats", lambda context: cognition_stats(runtime, context))
    runtime.commands.register("cardhawk.foundation.bootstrap", lambda context: cardhawk_foundation_bootstrap(runtime, context))
    runtime.commands.register("cardhawk.status", lambda context: cardhawk_status(runtime, context))
    runtime.commands.register("release.status", lambda context: release_status(runtime, context))
    runtime.commands.register("predict.stats", lambda context: predict_stats(runtime, context))
    runtime.commands.register("learn.snapshot", lambda context: learn_snapshot(runtime, context))
    runtime.commands.register("learn.stats", lambda context: learn_stats(runtime, context))
    runtime.commands.register("kernel.boot", lambda context: kernel_boot(runtime, context))
    runtime.commands.register("kernel.status", lambda context: kernel_status(runtime, context))
    runtime.commands.register("kernel.snapshot", lambda context: kernel_snapshot(runtime, context))
    runtime.commands.register("kernel.stats", lambda context: kernel_stats(runtime, context))
    runtime.commands.register("mission.v2.stats", lambda context: mission_v2_stats(runtime, context))
    runtime.commands.register("workflow.v2.stats", lambda context: workflow_v2_stats(runtime, context))
    runtime.commands.register("enterprise.bootstrap.cardhawk", lambda context: enterprise_bootstrap_cardhawk(runtime, context))
    runtime.commands.register("enterprise.stats", lambda context: enterprise_stats(runtime, context))
    runtime.commands.register("audit.history", lambda context: audit_history(runtime, context))
    runtime.commands.register("cluster.bootstrap", lambda context: cluster_bootstrap(runtime, context))
    runtime.commands.register("plugin.bootstrap", lambda context: plugin_bootstrap(runtime, context))
    runtime.commands.register("plugin.status", lambda context: plugin_status(runtime, context))
    runtime.commands.register("state.bootstrap", lambda context: state_bootstrap(runtime, context))
    runtime.commands.register("state.snapshot", lambda context: state_snapshot(runtime, context))
    runtime.commands.register("event.bootstrap", lambda context: event_bootstrap(runtime, context))
    runtime.commands.register("federation.bootstrap", lambda context: federation_bootstrap(runtime, context))
    runtime.commands.register("telemetry.bootstrap", lambda context: telemetry_bootstrap(runtime, context))
    runtime.commands.register("telemetry.metric", lambda context: telemetry_metric(runtime, context))
    runtime.commands.register("telemetry.health", lambda context: telemetry_health(runtime, context))
    runtime.commands.register("ha.bootstrap", lambda context: ha_bootstrap(runtime, context))
    runtime.commands.register("ha.status", lambda context: ha_status(runtime, context))
    runtime.commands.register("security.bootstrap", lambda context: security_bootstrap(runtime, context))
    runtime.commands.register("security.audit", lambda context: security_audit(runtime, context))
    runtime.commands.register("tenant.bootstrap", lambda context: tenant_bootstrap(runtime, context))
    runtime.commands.register("tenant.health", lambda context: tenant_health(runtime, context))
    runtime.commands.register("cluster.status", lambda context: cluster_status(runtime, context))
    runtime.commands.register("cluster.stats", lambda context: cluster_stats(runtime, context))
    runtime.commands.register("memory.mesh.snapshot", lambda context: memory_mesh_snapshot(runtime, context))
    runtime.commands.register("memory.mesh.stats", lambda context: memory_mesh_stats(runtime, context))
    runtime.commands.register("knowledge.bootstrap.cardhawk", lambda context: kg_bootstrap_cardhawk(runtime, context))
    runtime.commands.register("workflow.status", lambda context: workflow_status(runtime, context))
    runtime.commands.register("plan.bootstrap", lambda context: plan_bootstrap(runtime, context))
    runtime.commands.register("plan.status", lambda context: plan_status(runtime, context))


def cognition_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("cognition_stats", ((runtime.cognition.stats() if hasattr(runtime.cognition, 'stats') else runtime.cognition.statistics() if hasattr(runtime.cognition, 'statistics') else {'status': getattr(runtime.cognition, 'status', 'unknown')}) if hasattr(runtime.cognition, "stats") else runtime.cognition.statistics()))
    return context




def cardhawk_foundation_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    application = runtime.applications.register_card_hawk_foundation()
    runtime.knowledge.create_entity(
        label="Card Hawk Foundation™",
        entity_type="application",
        properties={
            "application_id": application.application_id,
            "version": application.version,
            "reference_implementation": True,
        },
    )
    runtime.memory.remember(
        key="cardhawk_foundation_bootstrapped",
        value=application.to_dict(),
        namespace="cardhawk.foundation",
        memory_type="persistent",
        tags=["cardhawk", "application", "foundation"],
    )
    context.add_result("application", application.to_dict())
    return context



def cardhawk_status(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.applications.health(name="Card Hawk Foundation™")
    context.add_result("cardhawk", result)
    return context



def release_status(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("release", runtime.release.status())
    return context



def predict_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("prediction_stats", ((runtime.prediction.stats() if hasattr(runtime.prediction, 'stats') else runtime.prediction.statistics() if hasattr(runtime.prediction, 'statistics') else {'status': getattr(runtime.prediction, 'status', 'unknown')}) if hasattr(runtime.prediction, "stats") else runtime.prediction.statistics()))
    return context




def learn_snapshot(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("snapshot", runtime.learning.snapshot())
    return context



def learn_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("learning_stats", ((runtime.learning.stats() if hasattr(runtime.learning, 'stats') else runtime.learning.statistics() if hasattr(runtime.learning, 'statistics') else {'status': getattr(runtime.learning, 'status', 'unknown')}) if hasattr(runtime.learning, "stats") else runtime.learning.statistics()))
    return context




def kernel_boot(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.kernel_v2.boot(self)
    context.add_result("kernel", result)
    return context



def kernel_status(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("kernel", runtime.kernel_v2.status())
    return context



def kernel_snapshot(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("snapshot", runtime.kernel_v2.snapshot())
    return context



def kernel_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("kernel_stats", ((runtime.kernel_v2.stats() if hasattr(runtime.kernel_v2, 'stats') else runtime.kernel_v2.statistics() if hasattr(runtime.kernel_v2, 'statistics') else {'status': getattr(runtime.kernel_v2, 'status', 'unknown')}) if hasattr(runtime.kernel_v2, "stats") else runtime.kernel_v2.statistics()))
    return context




def mission_v2_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("mission_v2_stats", ((runtime.mission_v2.stats() if hasattr(runtime.mission_v2, 'stats') else runtime.mission_v2.statistics() if hasattr(runtime.mission_v2, 'statistics') else {'status': getattr(runtime.mission_v2, 'status', 'unknown')}) if hasattr(runtime.mission_v2, "stats") else runtime.mission_v2.statistics()))
    return context




def workflow_v2_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("workflow_v2_stats", ((runtime.workflow_v2.stats() if hasattr(runtime.workflow_v2, 'stats') else runtime.workflow_v2.statistics() if hasattr(runtime.workflow_v2, 'statistics') else {'status': getattr(runtime.workflow_v2, 'status', 'unknown')}) if hasattr(runtime.workflow_v2, "stats") else runtime.workflow_v2.statistics()))
    return context




def enterprise_bootstrap_cardhawk(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    org = runtime.enterprise.bootstrap_cardhawk_enterprise()
    runtime.kernel_v2.publish(
        event_type="enterprise.cardhawk.bootstrapped",
        source="enterprise_core",
        payload=org.to_dict(),
    )
    context.add_result("enterprise", org.to_dict())
    return context



def enterprise_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("enterprise_stats", ((runtime.enterprise.stats() if hasattr(runtime.enterprise, 'stats') else runtime.enterprise.statistics() if hasattr(runtime.enterprise, 'statistics') else {'status': getattr(runtime.enterprise, 'status', 'unknown')}) if hasattr(runtime.enterprise, "stats") else runtime.enterprise.statistics()))
    return context



def audit_history(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("audit", runtime.enterprise.audit_history())
    return context




def cluster_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    cluster = runtime.distributed.bootstrap_primary_cluster()

    runtime.kernel_v2.publish(
        event_type="cluster.bootstrapped",
        source="distributed_fabric",
        payload=cluster.to_dict(),
    )

    # Return runtime statistics expected by the v3.0 tests
    context.add_result(
        "cluster",
        ((runtime.distributed.stats() if hasattr(runtime.distributed, 'stats') else runtime.distributed.statistics() if hasattr(runtime.distributed, 'statistics') else {'status': getattr(runtime.distributed, 'status', 'unknown')}) if hasattr(runtime.distributed, "stats") else runtime.distributed.statistics()),
    )

    return context



def plugin_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "plugin",
        runtime.plugins_v3.bootstrap(),
    )
    return context



def plugin_status(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "plugin_status",
        runtime.plugins_v3.status(),
    )
    return context



def state_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "state",
        runtime.persistence_v3.bootstrap(),
    )
    return context



def state_snapshot(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "snapshot",
        runtime.persistence_v3.snapshot(
            name=context.payload.get("name", "Runtime Snapshot"),
            runtime=self,
        ),
    )
    return context



def event_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "event_bus",
        runtime.event_bus_v3.bootstrap(),
    )
    return context



def federation_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "federation",
        runtime.federation_v3.bootstrap(),
    )
    return context



def telemetry_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "telemetry",
        runtime.telemetry_v3.bootstrap(),
    )
    return context



def telemetry_metric(runtime: Any, context: RuntimeContext) -> RuntimeContext:

    payload = context.payload

    context.add_result(
        "metric",
        runtime.telemetry_v3.metric(
            name=payload.get("name", "runtime.metric"),
            value=payload.get("value"),
            category=payload.get("category", "runtime"),
            metadata=payload.get("metadata", {}),
        ),
    )

    return context



def telemetry_health(runtime: Any, context: RuntimeContext) -> RuntimeContext:

    payload = context.payload

    context.add_result(
        "health",
        runtime.telemetry_v3.health(
            component=payload.get("component", "runtime"),
            status=payload.get("status", "healthy"),
        ),
    )

    return context



def ha_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("ha", runtime.high_availability_v3.bootstrap())
    return context



def ha_status(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("ha_status", runtime.high_availability_v3.status())
    return context



def security_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "security",
        runtime.security_v3.bootstrap(),
    )
    return context



def security_audit(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    payload = context.payload

    context.add_result(
        "audit",
        runtime.security_v3.audit(
            action=payload.get("action", "runtime"),
            actor=payload.get("actor", "system"),
            status=payload.get("status", "success"),
            metadata=payload.get("metadata", {}),
        ),
    )
    return context



def tenant_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "tenant",
        runtime.tenancy_v3.bootstrap(),
    )
    return context



def tenant_health(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "tenant_health",
        runtime.tenancy_v3.health(),
    )
    return context


# ==========================================================
# v4.0 Intelligence Kernel
# ==========================================================



def cluster_status(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.distributed.cluster_status(context.payload.get("cluster_id", ""))
    context.add_result("cluster_status", result)
    return context



def cluster_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("cluster_stats", ((runtime.distributed.stats() if hasattr(runtime.distributed, 'stats') else runtime.distributed.statistics() if hasattr(runtime.distributed, 'statistics') else {'status': getattr(runtime.distributed, 'status', 'unknown')}) if hasattr(runtime.distributed, "stats") else runtime.distributed.statistics()))
    return context



def memory_mesh_snapshot(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    result = runtime.memory_mesh.snapshot(context.payload.get("name", "Memory Mesh Snapshot"))
    context.add_result("snapshot", result)
    return context



def memory_mesh_stats(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("memory_mesh_stats", ((runtime.memory_mesh.stats() if hasattr(runtime.memory_mesh, 'stats') else runtime.memory_mesh.statistics() if hasattr(runtime.memory_mesh, 'statistics') else {'status': getattr(runtime.memory_mesh, 'status', 'unknown')}) if hasattr(runtime.memory_mesh, "stats") else runtime.memory_mesh.statistics()))
    return context




def kg_bootstrap_cardhawk(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("graph", runtime.knowledge_graph.bootstrap_cardhawk_graph())
    return context



def workflow_status(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("workflow_status", runtime.workflow_v3.status())
    return context



def plan_bootstrap(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result("planning", runtime.planning_v2.bootstrap())
    return context



def plan_status(runtime: Any, context: RuntimeContext) -> RuntimeContext:
    context.add_result(
        "plans",
        runtime.planning_v2.status(),
    )
    return context
