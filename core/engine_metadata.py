"""
Engine Metadata
"""

from dataclasses import dataclass


@dataclass
class EngineMetadata:
    name: str

    version: str

    author: str = "CardHawk"

    enabled: bool = True

    events: list | None = None
