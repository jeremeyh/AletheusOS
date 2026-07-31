"""
AletheusOS
Genesis 46.1

Cognitive Kernel™

Core Orchestration
"""

from __future__ import annotations

from aletheus.foundation_service_bus import foundation_service_bus
from aletheus.intent_engine import intent_engine

from .models import (
    CognitiveKernelRecord,
    new_kernel_record_id,
)


class CognitiveKernel:
    """
    The Cognitive Kernel coordinates governed cognition.

    It does not reason.
    It does not appraise.
    It does not deliberate.
    It conducts the first cognitive pathway:

    Query
        -> Intent Engine
        -> Foundation Service Bus
        -> Execution Plan
        -> Cognitive Kernel Record
    """

    GENESIS = "46.1"
    VERSION = "1.0.0"

    def __init__(self) -> None:
        self._records: list[CognitiveKernelRecord] = []

    def process(
        self,
        *,
        identity: str,
        application: str,
        query: str,
        context: dict | None = None,
        constraints: list[str] | None = None,
        priority: str = "normal",
    ) -> CognitiveKernelRecord:

        intent = intent_engine.resolve(
            identity=identity,
            application=application,
            query=query,
            context=context,
            constraints=constraints,
            priority=priority,
        )

        resolution = foundation_service_bus.resolve(intent.capability_request)

        record = CognitiveKernelRecord(
            kernel_record_id=new_kernel_record_id(),
            identity=identity,
            application=application,
            query=query,
            intent=intent.to_dict(),
            capability_resolution=resolution.to_dict(),
            execution_plan=(
                resolution.execution_plan.to_dict()
                if resolution.execution_plan
                else None
            ),
            constitutional_articles=[
                "Principle X",
                "Intent Before Execution",
                "Applications Request Capabilities",
                "Canonical Intelligence Objects",
                "Orchestration Before Implementation",
                "Proof Before Promotion",
                "Elegant Sufficiency",
            ],
            status="PROCESSING",
        )

        record.add_step(
            stage="intent_resolution",
            engine="intent_engine",
            status="completed",
            metadata={
                "intent_type": intent.intent_type,
                "capability_request": intent.capability_request,
                "confidence": intent.confidence,
            },
        )

        record.add_step(
            stage="capability_resolution",
            engine="foundation_service_bus",
            status="completed" if resolution.resolved else "failed",
            metadata={
                "resolved": resolution.resolved,
                "capability_id": resolution.capability_id,
                "engine_id": resolution.engine_id,
                "confidence": resolution.confidence,
            },
        )

        if resolution.execution_plan:
            record.add_step(
                stage="execution_plan_selection",
                engine="foundation_service_bus",
                status="completed",
                metadata={
                    "plan_id": resolution.execution_plan.plan_id,
                    "stages": len(resolution.execution_plan.stages),
                },
            )
        else:
            record.add_step(
                stage="execution_plan_selection",
                engine="foundation_service_bus",
                status="skipped",
                metadata={
                    "reason": "No execution plan available for resolved capability.",
                    "capability_request": intent.capability_request,
                },
            )

        record.mark_completed()

        self._records.append(record)

        return record

    def records(self) -> list[dict]:
        return [record.to_dict() for record in self._records]

    def health(self) -> dict:
        return {
            "name": "Cognitive Kernel",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "records": len(self._records),
            "intent_engine": intent_engine.health(),
            "foundation_service_bus": foundation_service_bus.health(),
        }

    def statistics(self) -> dict:
        return {
            "name": "Cognitive Kernel",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "records": len(self._records),
        }


cognitive_kernel = CognitiveKernel()
