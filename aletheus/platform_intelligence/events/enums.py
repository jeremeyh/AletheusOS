"""Canonical event classifications for the Platform Intelligence Fabric."""

from __future__ import annotations

from enum import StrEnum


class ConstitutionalEventKind(StrEnum):
    """Canonical kinds of constitutional facts."""

    PLATFORM_STARTED = "platform.started"
    PLATFORM_STOPPED = "platform.stopped"

    OBJECT_REGISTERED = "object.registered"
    OBJECT_UPDATED = "object.updated"
    OBJECT_RETIRED = "object.retired"

    STATE_CHANGED = "state.changed"
    HEALTH_CHANGED = "health.changed"

    RELATIONSHIP_CREATED = "relationship.created"
    RELATIONSHIP_REMOVED = "relationship.removed"

    SERVICE_REGISTERED = "service.registered"
    SERVICE_STARTED = "service.started"
    SERVICE_STOPPED = "service.stopped"
    SERVICE_FAILED = "service.failed"

    CAPABILITY_REGISTERED = "capability.registered"
    CAPABILITY_ACTIVATED = "capability.activated"
    CAPABILITY_DEACTIVATED = "capability.deactivated"

    DEPENDENCY_RESOLVED = "dependency.resolved"
    DEPENDENCY_FAILED = "dependency.failed"

    POLICY_EVALUATED = "policy.evaluated"
    GOVERNANCE_VIOLATION = "governance.violation"

    BUILD_STARTED = "build.started"
    BUILD_COMPLETED = "build.completed"
    BUILD_FAILED = "build.failed"

    APPLICATION_LOADED = "application.loaded"
    APPLICATION_UNLOADED = "application.unloaded"

    WORKSPACE_CREATED = "workspace.created"
    WORKSPACE_ACTIVATED = "workspace.activated"
    WORKSPACE_CLOSED = "workspace.closed"


class ConstitutionalEventSeverity(StrEnum):
    """Operational significance of a constitutional event."""

    TRACE = "trace"
    INFO = "info"
    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
