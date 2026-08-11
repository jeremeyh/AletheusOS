from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class LearningExperience:
    event_type: str
    description: str
    source: str = "aletheus"
    outcome: str = "unknown"
    confidence: float = 0.75
    metadata: dict[str, Any] = field(default_factory=dict)
    experience_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class LearnedLesson:
    title: str
    lesson: str
    source_experience_id: str = ""
    confidence: float = 0.75
    tags: list[str] = field(default_factory=list)
    lesson_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class LearnedPattern:
    title: str
    pattern: str
    frequency: int = 1
    confidence: float = 0.75
    pattern_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class ImprovementSuggestion:
    title: str
    suggestion: str
    priority: str = "medium"
    expected_gain: float = 0.1
    confidence: float = 0.75
    suggestion_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
