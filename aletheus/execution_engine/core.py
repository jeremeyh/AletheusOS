from __future__ import annotations

from .models import (
    ExecutionRecord,
    new_execution_id,
)

from aletheus.identity_engine import identity_resolver
from aletheus.capability_engine import capability_engine
from aletheus.foundation import aletheus_foundation
from aletheus.aos_search import aos_search
from aletheus.runtime import runtime_core


class AletheusExecutionEngine:

    GENESIS = "25.1"
    VERSION = "1.1.0"

    def execute(
        self,
        identity: str,
        application: str,
        query: str,
    ) -> ExecutionRecord:

        record = ExecutionRecord(
            execution_id=new_execution_id(),
            identity=identity,
            application=application,
            query=query,
        )

        #
        # Execution Started
        #

        runtime_core.events.publish(
            "execution.started",
            {
                "execution_id": record.execution_id,
                "identity": identity,
                "application": application,
                "query": query,
            },
            source="execution_engine",
        )

        #
        # Resolve Identity
        #

        resolved = identity_resolver.resolve(identity)

        if resolved:

            record.metadata["identity"] = resolved.to_dict()

            runtime_core.events.publish(
                "identity.resolved",
                {
                    "execution_id": record.execution_id,
                    "identity": identity,
                },
                source="identity_engine",
            )

        #
        # Capability Health
        #

        record.metadata["capability"] = capability_engine.health()

        runtime_core.events.publish(
            "capability.resolved",
            {
                "execution_id": record.execution_id,
            },
            source="capability_engine",
        )

        #
        # Foundation Health
        #

        record.metadata["foundation"] = (
            aletheus_foundation.health()
        )

        #
        # Search Planning
        #

        search = aos_search.execute(query)

        runtime_core.events.publish(
            "search.planned",
            {
                "execution_id": record.execution_id,
                "query": query,
            },
            source="aos_search",
        )

        record.result = search

        record.status = "completed"

        #
        # Execution Complete
        #

        runtime_core.events.publish(
            "execution.completed",
            {
                "execution_id": record.execution_id,
                "status": record.status,
            },
            source="execution_engine",
        )

        return record

    def health(self):

        return {
            "name": "Execution Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


execution_engine = AletheusExecutionEngine()
