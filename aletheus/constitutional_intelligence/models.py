"""
Constitutional Models

Genesis 13.54
"""

from dataclasses import dataclass, field


@dataclass
class Principle:
    principle_id: str

    name: str

    description: str

    immutable: bool = True


@dataclass
class GovernanceDecision:
    action: str

    approved: bool

    reasoning: list = field(default_factory=list)
