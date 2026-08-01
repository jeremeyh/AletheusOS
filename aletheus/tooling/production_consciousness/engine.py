from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    prompt: str
    answer: str
    evidence: tuple[str, ...]


class Engine:
    def synthesize(
        self,
        *,
        changed: str,
        reason: str,
        constitutional: bool,
        safe: bool,
        quality_delta: float,
        risk_delta: float,
        recommendation: str,
        evidence: tuple[str, ...],
    ) -> dict[str, object]:
        questions = (
            Question("What changed?", changed, evidence),
            Question("Why did it change?", reason, evidence),
            Question(
                "Was it constitutional?",
                "yes" if constitutional else "no",
                evidence,
            ),
            Question("Was it safe?", "yes" if safe else "no", evidence),
            Question("Did quality improve?", str(quality_delta >= 0), evidence),
            Question("Did risk increase?", str(risk_delta > 0), evidence),
            Question("What should happen next?", recommendation, evidence),
        )
        return {
            "self_model": [
                {
                    "prompt": item.prompt,
                    "answer": item.answer,
                    "evidence": list(item.evidence),
                }
                for item in questions
            ],
            "constitutional": constitutional,
            "safe": safe,
            "recommendation": recommendation,
            "status": "self_explained",
        }
