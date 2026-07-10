from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from typing import Any, Dict, List

from aletheus.cognition.models import Goal, Plan, ReasoningSession, Decision


class AletheusCognitionCore:
    def __init__(self) -> None:
        self.version = "0.5.0-genesis"
        self.goals: List[Goal] = []
        self.plans: List[Plan] = []
        self.reasoning_sessions: List[ReasoningSession] = []
        self.decisions: List[Decision] = []

    def create_goal(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        owner: str = "Founder",
        application: str = "system",
    ) -> Goal:
        goal = Goal(
            title=title,
            description=description,
            priority=priority,
            owner=owner,
            application=application,
        )
        self.goals.append(goal)
        return goal

    def complete_goal(self, goal_id: str) -> Dict[str, Any]:
        for goal in self.goals:
            if goal.goal_id == goal_id:
                goal.status = "completed"
                goal.completed_at = __import__("datetime").utc_now_iso()
                return goal.to_dict()
        return {"error": f"Goal not found: {goal_id}"}

    def list_goals(self, status: str | None = None) -> List[Dict[str, Any]]:
        results = self.goals
        if status:
            results = [goal for goal in results if goal.status == status]
        return [goal.to_dict() for goal in results]

    def generate_plan(self, goal_id: str, goal_title: str = "") -> Plan:
        title = goal_title or "Untitled Goal"
        lower_title = title.lower()

        if "portfolio" in lower_title or "card" in lower_title:
            steps = [
                "Refresh marketplace intelligence.",
                "Identify underpriced scarce assets.",
                "Run THORᵡ opportunity scoring.",
                "Run DEF decision framework.",
                "Rank acquisition candidates.",
                "Record recommendation and rationale.",
            ]
        else:
            steps = [
                "Clarify objective.",
                "Identify required information.",
                "Evaluate available evidence.",
                "Generate options.",
                "Recommend next action.",
            ]

        plan = Plan(goal_id=goal_id, title=f"Plan for {title}", steps=steps)
        self.plans.append(plan)
        return plan

    def list_plans(self) -> List[Dict[str, Any]]:
        return [plan.to_dict() for plan in self.plans]

    def reason(
        self,
        prompt: str,
        evidence: List[str] | None = None,
        assumptions: List[str] | None = None,
    ) -> ReasoningSession:
        evidence = evidence or []
        assumptions = assumptions or []

        confidence = 0.72
        if evidence:
            confidence += min(len(evidence) * 0.04, 0.2)
        if assumptions:
            confidence -= min(len(assumptions) * 0.02, 0.1)

        confidence = round(max(0.0, min(confidence, 0.98)), 2)

        conclusion = "Proceed with structured evaluation before execution."
        recommended_actions = [
            "Gather additional signal.",
            "Run applicable engines.",
            "Record decision rationale.",
        ]
        risks = [
            "Incomplete information.",
            "Overconfidence without external validation.",
        ]

        session = ReasoningSession(
            prompt=prompt,
            conclusion=conclusion,
            confidence=confidence,
            evidence=evidence,
            assumptions=assumptions,
            risks=risks,
            recommended_actions=recommended_actions,
        )
        self.reasoning_sessions.append(session)
        return session

    def list_reasoning_sessions(self) -> List[Dict[str, Any]]:
        return [session.to_dict() for session in self.reasoning_sessions]

    def record_decision(
        self,
        title: str,
        decision: str,
        rationale: str,
        confidence: float = 0.75,
        evidence: List[str] | None = None,
    ) -> Decision:
        item = Decision(
            title=title,
            decision=decision,
            rationale=rationale,
            confidence=confidence,
            evidence=evidence or [],
        )
        self.decisions.append(item)
        return item

    def decision_history(self) -> List[Dict[str, Any]]:
        return [decision.to_dict() for decision in self.decisions]

    def stats(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "goals": len(self.goals),
            "active_goals": len([goal for goal in self.goals if goal.status == "active"]),
            "plans": len(self.plans),
            "reasoning_sessions": len(self.reasoning_sessions),
            "decisions": len(self.decisions),
        }


cognition_core = AletheusCognitionCore()
