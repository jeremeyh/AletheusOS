from __future__ import annotations

from .immutable_snapshot import (
    ImmutableRuntimeSnapshot,
)


class RuntimeSnapshotBuilder:

    VERSION="1.0.0"

    def build(

        self,

        topology,

        provider_manager,

        health_engine,

        diagnostics,

    ):

        health=health_engine.evaluate(

            topology,

            provider_manager,

        )

        return ImmutableRuntimeSnapshot(

            topology=topology.snapshot(),

            providers=provider_manager.snapshot(),

            health=health,

            diagnostics=diagnostics,

            version=self.VERSION,
        )
