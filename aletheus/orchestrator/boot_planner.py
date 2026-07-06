from __future__ import annotations

from .boot_plan import BootPlan
from .component_graph import ComponentGraph


class BootPlanner:
    """
    Boot Planner™

    Produces a deterministic boot sequence from the
    platform dependency graph.

    Genesis 6.10
    """

    GENESIS = "6.10"
    VERSION = "0.1.0"

    def __init__(self, graph: ComponentGraph):
        self.graph = graph

    def create_plan(self) -> BootPlan:

        plan = BootPlan()

        #
        # Phase 1
        #
        # Simple deterministic ordering.
        #
        # Genesis 7 will replace this with a
        # full dependency resolver.
        #

        plan.components.extend(sorted(self.graph.nodes()))

        return plan

    def health(self):

        return {
            "name": "Boot Planner",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
        }
