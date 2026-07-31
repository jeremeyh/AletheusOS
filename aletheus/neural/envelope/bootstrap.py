from __future__ import annotations


class Bootstrap:
    """
    Bootstrap™

    Responsible only for constructing the default
    Neural Envelope architecture.
    """

    VERSION = "0.1.0"

    def __init__(self, brain):
        self.brain = brain

    def run(self):

        self._cortices()
        self._neurons()
        self._synapses()

    def _cortices(self):

        defaults = [
            ("executive", "Executive Cortex", "governance"),
            ("memory", "Memory Cortex", "memory"),
            ("reasoning", "Reasoning Cortex", "reasoning"),
            ("planning", "Planning Cortex", "planning"),
            ("perception", "Perception Cortex", "perception"),
            ("communication", "Communication Cortex", "communication"),
            ("immune", "Immune System", "integrity"),
        ]

        for id, name, role in defaults:
            if id not in self.brain.cortex._cortices:
                self.brain.cortex.register(
                    id=id,
                    name=name,
                    role=role,
                    status="online",
                )

    def _neurons(self):

        defaults = [
            ("founder_console", "Founder Console", "executive"),
            ("executive_kernel", "Executive Kernel", "executive"),
            ("council", "Council", "executive"),
            ("reasoning", "Reasoning", "reasoning"),
            ("decision", "Decision", "reasoning"),
            ("prediction", "Prediction", "reasoning"),
            ("memory", "Memory", "memory"),
            ("knowledge", "Knowledge", "memory"),
            ("semantic", "Semantic", "memory"),
            ("planning", "Planning", "planning"),
            ("mission", "Mission", "planning"),
            ("workflow", "Workflow", "planning"),
            ("hawk_a_eye", "Hawk A•eye", "perception"),
            ("communications", "Communications", "communication"),
            ("guardian", "Guardian", "immune"),
            ("conclave", "Conclave", "immune"),
            ("watch_tower", "Watch Tower", "immune"),
            ("sentinel", "Sentinel", "immune"),
        ]

        for id, name, cortex in defaults:
            if self.brain.neurons.get(id) is None:
                self.brain.neurons.register(
                    id=id,
                    name=name,
                    cortex=cortex,
                    package="internal",
                    role=name,
                    status="online",
                )

    def _synapses(self):

        defaults = [
            ("syn-immune-executive", "guardian", "executive_kernel"),
            ("syn-reasoning-memory", "reasoning", "memory"),
            ("syn-reasoning-knowledge", "reasoning", "knowledge"),
            ("syn-prediction-planning", "prediction", "planning"),
            ("syn-planning-mission", "planning", "mission"),
            ("syn-perception-reasoning", "hawk_a_eye", "reasoning"),
            ("syn-council-founder", "council", "founder_console"),
        ]

        for id, source, target in defaults:
            if id not in self.brain.synapses._synapses:
                self.brain.synapses.register(
                    id=id,
                    source=source,
                    target=target,
                    purpose="bootstrap",
                    status="active",
                )
