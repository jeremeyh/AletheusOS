from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class VocabularyTerm:
    name: str
    meaning: str
    tier: str
    domain_family: str
    canonical: bool = True
    aliases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CapabilityMapping:
    platform_capability: str
    application_capability: str
    experience_name: str
    semantic_contract: str
    allowed_applications: tuple[str, ...] = ("CARD_HAWK",)


@dataclass(frozen=True, slots=True)
class VocabularyLibrary:
    library_id: str
    version: str
    terms: tuple[VocabularyTerm, ...]
    mappings: tuple[CapabilityMapping, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
