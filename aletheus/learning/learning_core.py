from __future__ import annotations

from typing import Any

from aletheus.learning.models import (
    ImprovementSuggestion,
    LearnedLesson,
    LearnedPattern,
    LearningExperience,
)


class AletheusAdaptiveLearning:
    def __init__(self) -> None:
        self.version = "1.8.0"
        self.experiences: list[LearningExperience] = []
        self.lessons: list[LearnedLesson] = []
        self.pattern_history: list[LearnedPattern] = []
        self.improvements: list[ImprovementSuggestion] = []

    def record_experience(
        self,
        event_type: str,
        description: str,
        source: str = "aletheus",
        outcome: str = "unknown",
        confidence: float = 0.75,
        metadata: dict[str, Any] | None = None,
    ) -> LearningExperience:
        item = LearningExperience(
            event_type=event_type,
            description=description,
            source=source,
            outcome=outcome,
            confidence=confidence,
            metadata=metadata or {},
        )
        self.experiences.append(item)
        return item

    def create_lesson(
        self,
        title: str,
        lesson: str,
        source_experience_id: str = "",
        confidence: float = 0.75,
        tags: list[str] | None = None,
    ) -> LearnedLesson:
        item = LearnedLesson(
            title=title,
            lesson=lesson,
            source_experience_id=source_experience_id,
            confidence=confidence,
            tags=tags or [],
        )
        self.lessons.append(item)
        return item

    def feedback(
        self,
        experience_id: str,
        outcome: str,
        lesson: str = "",
        confidence: float = 0.8,
    ) -> dict[str, Any]:
        experience = next(
            (item for item in self.experiences if item.experience_id == experience_id),
            None,
        )

        if experience is None:
            return {"error": f"Experience not found: {experience_id}"}

        experience.outcome = outcome
        experience.confidence = confidence

        created_lesson = None
        if lesson:
            created_lesson = self.create_lesson(
                title=f"Lesson from {experience.event_type}",
                lesson=lesson,
                source_experience_id=experience.experience_id,
                confidence=confidence,
                tags=[experience.event_type, outcome],
            )

        return {
            "experience": experience.to_dict(),
            "lesson": created_lesson.to_dict() if created_lesson else None,
        }

    def discover_patterns(self) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}

        for experience in self.experiences:
            key = f"{experience.event_type}:{experience.outcome}"
            counts[key] = counts.get(key, 0) + 1

        patterns: list[LearnedPattern] = []

        for key, count in counts.items():
            event_type, outcome = key.split(":", 1)
            pattern = LearnedPattern(
                title=f"{event_type} tends toward {outcome}",
                pattern=f"Aletheus has observed {count} experience(s) where {event_type} resulted in {outcome}.",
                frequency=count,
                confidence=round(min(0.65 + (count * 0.05), 0.95), 2),
            )
            patterns.append(pattern)

        self.pattern_history.extend(patterns)
        return [item.to_dict() for item in patterns]

    def improve(self, runtime: Any) -> list[dict[str, Any]]:
        health = runtime.commands.dispatch("runtime.health", {}).results.get("health", {})
        suggestions: list[ImprovementSuggestion] = []

        if health.get("memory_records", 0) < 10:
            suggestions.append(
                ImprovementSuggestion(
                    title="Increase learning memory density",
                    suggestion="Capture more plans, predictions, decisions, feedback, and outcomes so Aletheus has enough experience to improve future reasoning.",
                    priority="high",
                    expected_gain=0.21,
                    confidence=0.88,
                )
            )

        if health.get("semantic_concepts", 0) < 5:
            suggestions.append(
                ImprovementSuggestion(
                    title="Seed semantic knowledge",
                    suggestion="Bootstrap Card Hawk semantic concepts and add player, asset, service, and decision concepts.",
                    priority="high",
                    expected_gain=0.24,
                    confidence=0.9,
                )
            )

        if health.get("active_plans", 0) == 0:
            suggestions.append(
                ImprovementSuggestion(
                    title="Create active adaptive plan",
                    suggestion="Use the planning engine to create an active plan so the learning engine can evaluate execution quality.",
                    priority="medium",
                    expected_gain=0.16,
                    confidence=0.84,
                )
            )

        if not suggestions:
            suggestions.append(
                ImprovementSuggestion(
                    title="Continue adaptive expansion",
                    suggestion="System learning baseline is acceptable. Continue feeding mission outcomes, predictive results, and founder feedback into Adaptive Learning.",
                    priority="medium",
                    expected_gain=0.12,
                    confidence=0.8,
                )
            )

        self.improvements.extend(suggestions)
        return [item.to_dict() for item in suggestions]

    def snapshot(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "stats": self.stats(),
            "recent_experiences": [item.to_dict() for item in self.experiences[-10:]],
            "recent_lessons": [item.to_dict() for item in self.lessons[-10:]],
            "recent_patterns": [item.to_dict() for item in self.pattern_history[-10:]],
            "recent_improvements": [item.to_dict() for item in self.improvements[-10:]],
        }

    def stats(self) -> dict[str, Any]:
        total_confidence = sum(item.confidence for item in self.experiences)
        learning_score = 0.0
        if self.experiences:
            learning_score = round(total_confidence / len(self.experiences), 2)

        return {
            "version": self.version,
            "experiences": len(self.experiences),
            "lessons": len(self.lessons),
            "patterns": len(self.pattern_history),
            "improvements": len(self.improvements),
            "learning_score": learning_score,
        }


learning_core = AletheusAdaptiveLearning()
