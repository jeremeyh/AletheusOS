"""
Card Hawk Command Center Models

Genesis 13.14
"""

from dataclasses import dataclass, field


@dataclass
class DashboardState:

    portfolio: dict = field(
        default_factory=dict
    )

    intelligence: dict = field(
        default_factory=dict
    )

    alerts: list = field(
        default_factory=list
    )

    opportunities: list = field(
        default_factory=list
    )

