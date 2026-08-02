from __future__ import annotations

from dataclasses import replace

from .models import NavigationContext


class Engine:
    def propagate(
        self, context: NavigationContext, destination: str
    ) -> NavigationContext:
        return replace(
            context,
            current_node=destination,
            history=context.history + (context.current_node,),
        )

    def attach_asset(
        self, context: NavigationContext, asset_id: str
    ) -> NavigationContext:
        return replace(context, asset_id=asset_id)

    def attach_evidence(
        self, context: NavigationContext, evidence_id: str
    ) -> NavigationContext:
        return (
            context
            if evidence_id in context.evidence_ids
            else replace(context, evidence_ids=context.evidence_ids + (evidence_id,))
        )
