"""
Cognitive Reasoning Models

Genesis 13.52
"""

from dataclasses import dataclass, field



@dataclass
class CognitiveContext:


    intent: str

    information: dict = field(
        default_factory=dict
    )



@dataclass
class ReasoningResult:


    conclusion: str

    confidence: int

    explanation: list = field(
        default_factory=list
    )

