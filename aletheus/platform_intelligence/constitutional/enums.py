"""Canonical enumerations for the Constitutional Knowledge Model."""

from __future__ import annotations

from enum import StrEnum


class ConstitutionalKind(StrEnum):
    """Kinds of objects constitutionally recognized by AletheusOS."""

    RUNTIME = "runtime"
    PLATFORM_SERVICE = "platform_service"
    REGISTRY = "registry"
    CAPABILITY = "capability"
    WORKSPACE = "workspace"
    APPLICATION = "application"
    EXPERIENCE = "experience"
    PRIMITIVE = "primitive"
    THEME = "theme"
    NAVIGATION = "navigation"
    INSTRUMENT = "instrument"
    ENGINE = "engine"
    BUILD = "build"
    RELEASE = "release"
    POLICY = "policy"
    EVENT = "event"
    SESSION = "session"
    USER = "user"


class ConstitutionalState(StrEnum):
    """Canonical lifecycle shared by all constitutional objects."""

    REGISTERED = "registered"
    INITIALIZING = "initializing"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    DEGRADED = "degraded"
    RECOVERING = "recovering"
    STOPPING = "stopping"
    STOPPED = "stopped"
    RETIRED = "retired"


class ConstitutionalHealth(StrEnum):
    """Canonical health vocabulary for the Platform Intelligence Fabric."""

    HEALTHY = "healthy"
    WARNING = "warning"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class RelationshipKind(StrEnum):
    """Semantic relationships supported by the Constitutional Graph."""

    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    PROVIDES = "provides"
    USES = "uses"
    EXTENDS = "extends"
    GOVERNED_BY = "governed_by"
    PUBLISHED_BY = "published_by"
    SUBSCRIBES_TO = "subscribes_to"
    HOSTS = "hosts"
    OWNS = "owns"
    REALIZES = "realizes"
    REALIZED_BY = "realized_by"
    OBSERVES = "observes"
    GENERATES = "generates"
    REQUIRES = "requires"
    REGISTERED_IN = "registered_in"
