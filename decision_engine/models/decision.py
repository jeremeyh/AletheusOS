from dataclasses import asdict, dataclass


@dataclass
class DecisionReport:
    asset_id: int
    player: str
    qdef_score: float
    ddef_score: float
    final_score: float
    recommendation: str
    confidence: float
    strike_zone: str
    explanation: list

    def to_dict(self):
        return asdict(self)
