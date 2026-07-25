"""SPAN™ domain events."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from .models import utc_now


class SPANEventType(str, Enum):
    STARTED = "span.started"
    STOPPED = "span.stopped"
    ANALYSIS_COMPLETED = "span.analysis.completed"
    RECOMMENDATION_CREATED = "span.recommendation.created"
    RECOMMENDATION_RECORDED = "span.recommendation.recorded"


@dataclass(frozen=True, slots=True)
class SPANEvent:
    event_type: SPANEventType
    aggregate_id: UUID | None = None
    payload: Mapping[str, Any] = field(default_factory=dict)
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=utc_now)
