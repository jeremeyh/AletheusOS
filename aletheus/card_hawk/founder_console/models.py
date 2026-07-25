"""
Founder Console Models

Genesis 13.32
"""

from dataclasses import dataclass, field


@dataclass
class ConsoleWidget:


    name: str

    status: str = "active"

    data: dict = field(
        default_factory=dict
    )

