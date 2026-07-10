from __future__ import annotations


class LearningDomain:
    """
    Learning capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def record(self, context):
        payload = context.payload

        experience = self.runtime.learning.record_experience(
            event_type=payload.get("event_type", "general"),
            description=payload.get("description", ""),
            source=payload.get("source", context.application),
            outcome=payload.get("outcome", "unknown"),
            confidence=float(payload.get("confidence", 0.75)),
            metadata=payload.get("metadata", {}),
        )

        self.runtime.memory.remember(
            key="learning_experience",
            value=experience.to_dict(),
            namespace="aletheus.learning",
            memory_type="episodic",
            tags=["learning", "experience"],
        )

        context.add_result("experience", experience.to_dict())
        return context

    def lesson(self, context):
        payload = context.payload

        lesson = self.runtime.learning.create_lesson(
            title=payload.get("title", "Untitled Lesson"),
            lesson=payload.get("lesson", ""),
            source_experience_id=payload.get("source_experience_id", ""),
            confidence=float(payload.get("confidence", 0.75)),
            tags=payload.get("tags", []),
        )

        self.runtime.memory.remember(
            key="learned_lesson",
            value=lesson.to_dict(),
            namespace="aletheus.learning",
            memory_type="semantic",
            tags=["learning", "lesson"],
        )

        context.add_result("lesson", lesson.to_dict())
        return context

    def feedback(self, context):
        payload = context.payload

        result = self.runtime.learning.feedback(
            experience_id=payload.get("experience_id", ""),
            outcome=payload.get("outcome", "unknown"),
            lesson=payload.get("lesson", ""),
            confidence=float(payload.get("confidence", 0.8)),
        )

        context.add_result("feedback", result)
        return context

    def patterns(self, context):
        context.add_result(
            "patterns",
            self.runtime.learning.discover_patterns(),
        )
        return context

    def improve(self, context):
        context.add_result(
            "improvements",
            self.runtime.learning.improve(self.runtime),
        )
        return context

    def snapshot(self, context):
        context.add_result(
            "snapshot",
            self.runtime.learning.snapshot(),
        )
        return context

    def statistics(self, context):
        context.add_result(
            "learning_stats",
            (
                self.runtime.learning.stats()
                if hasattr(self.runtime.learning, "stats")
                else self.runtime.learning.statistics()
            ),
        )
        return context
