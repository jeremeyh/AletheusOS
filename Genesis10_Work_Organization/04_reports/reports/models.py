"""
Card Hawk Report Models

Genesis 13.18
"""

from dataclasses import dataclass, field


@dataclass
class IntelligenceReport:


    report_type: str

    title: str

    summary: str

    data: dict = field(
        default_factory=dict
    )


