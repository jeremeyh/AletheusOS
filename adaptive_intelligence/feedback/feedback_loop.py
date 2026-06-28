from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class RecommendationFeedback:
    recommendation_type: str
    subject: str
    recommendation: str
    accepted: bool | None = None
    actual_outcome: str = ""
    predicted_value: float = 0.0
    actual_value: float = 0.0
    notes: str = ""
    feedback_id: str = field(default_factory=lambda: f"FB-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class IntelligenceFeedbackLoop:
    """7.0A — Intelligence Feedback Loop™."""
    _feedback = []

    @classmethod
    def record(cls, recommendation_type, subject, recommendation, accepted=None, predicted_value=0, actual_value=0, actual_outcome="", notes=""):
        item = RecommendationFeedback(
            recommendation_type=recommendation_type,
            subject=subject,
            recommendation=recommendation,
            accepted=accepted,
            predicted_value=float(predicted_value or 0),
            actual_value=float(actual_value or 0),
            actual_outcome=actual_outcome,
            notes=notes,
        )
        cls._feedback.append(item)
        return item

    @classmethod
    def all(cls):
        return cls._feedback

    @classmethod
    def metrics(cls):
        total = len(cls._feedback)
        accepted = len([x for x in cls._feedback if x.accepted is True])
        rejected = len([x for x in cls._feedback if x.accepted is False])
        with_actuals = [x for x in cls._feedback if x.actual_value and x.predicted_value]
        prediction_error = 0
        if with_actuals:
            prediction_error = sum(abs(x.actual_value - x.predicted_value) for x in with_actuals) / len(with_actuals)
        return {
            "total_feedback": total,
            "accepted": accepted,
            "rejected": rejected,
            "acceptance_rate": (accepted / total * 100) if total else 0,
            "avg_prediction_error": round(prediction_error, 2),
        }
