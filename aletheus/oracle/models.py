from dataclasses import dataclass


@dataclass
class Forecast:
    category: str
    confidence: float
    summary: str
