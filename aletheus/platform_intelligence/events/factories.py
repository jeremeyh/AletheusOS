"""Canonical factories for common platform events."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalHealth,
    ConstitutionalObject,
    ConstitutionalState,
)

from .enums import ConstitutionalEventKind
from .event import ConstitutionalEvent


def object_registered_event(
    obj: ConstitutionalObject,
    *,
    source: str = "service.platform-registry",
) -> ConstitutionalEvent:
    return ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.OBJECT_REGISTERED,
        source=source,
        subject=obj.identity.address,
        payload={
            "object": obj.to_snapshot(),
        },
    )


def state_changed_event(
    obj: ConstitutionalObject,
    *,
    previous_state: ConstitutionalState,
    source: str = "service.lifecycle",
) -> ConstitutionalEvent:
    return ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.STATE_CHANGED,
        source=source,
        subject=obj.identity.address,
        payload={
            "previous_state": previous_state.value,
            "current_state": obj.state.value,
        },
    )


def health_changed_event(
    obj: ConstitutionalObject,
    *,
    previous_health: ConstitutionalHealth,
    source: str = "service.health",
    metadata: Mapping[str, Any] | None = None,
) -> ConstitutionalEvent:
    return ConstitutionalEvent.create(
        kind=ConstitutionalEventKind.HEALTH_CHANGED,
        source=source,
        subject=obj.identity.address,
        payload={
            "previous_health": previous_health.value,
            "current_health": obj.health.value,
            "metrics": dict(obj.metrics),
        },
        metadata=metadata,
    )
