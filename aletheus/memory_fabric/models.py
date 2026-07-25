"""
Memory Fabric Models

Genesis 13.47
"""

from dataclasses import dataclass, field


@dataclass
class MemoryRecord:


    memory_id: str

    memory_type: str

    content: dict

    confidence: int = 0

    provenance: dict = field(
        default_factory=dict
    )

