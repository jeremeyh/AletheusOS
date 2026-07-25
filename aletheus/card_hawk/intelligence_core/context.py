"""
Card Hawk Intelligence Context

Genesis 13.11
"""

from dataclasses import dataclass, field


@dataclass
class IntelligenceContext:

    asset_id: str

    signals: dict = field(
        default_factory=dict
    )

    analysis: dict = field(
        default_factory=dict
    )

    decisions: dict = field(
        default_factory=dict
    )

