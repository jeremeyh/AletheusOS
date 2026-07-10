"""
Anchor Evolution Analytics Engine

Genesis 8.24

Analyzes evolution trajectory.
"""


import time



class AnchorEvolutionAnalyticsEngine:


    def __init__(
        self,
        evolution_graph,
        intelligence
    ):

        self.evolution_graph = evolution_graph
        self.intelligence = intelligence

        self.reports = []



    def analyze(
        self
    ):

        graph = (
            self.evolution_graph
            .snapshot()
        )


        node_count = (
            graph["nodes"]
        )

        relationship_count = (
            graph["relationships"]
        )


        velocity = self.calculate_velocity(
            node_count
        )


        stability = self.calculate_stability(
            relationship_count,
            node_count
        )


        report = {

            "graph_size":
            {
                "nodes":
                    node_count,

                "relationships":
                    relationship_count

            },

            "evolution_velocity":
                velocity,

            "stability_score":
                stability,

            "trajectory":
                self.determine_direction(
                    velocity,
                    stability
                ),

            "timestamp":
                time.time()

        }


        self.reports.append(report)


        return report



    def calculate_velocity(
        self,
        nodes
    ):

        if nodes == 0:

            return 0


        return min(
            nodes * 10,
            100
        )



    def calculate_stability(
        self,
        relationships,
        nodes
    ):

        if nodes == 0:

            return 100


        return min(
            int(
                (
                    relationships
                    /
                    nodes
                )
                * 100
            ),
            100
        )



    def determine_direction(
        self,
        velocity,
        stability
    ):

        if (
            velocity >= 70
            and
            stability >= 50
        ):

            return "accelerating_growth"


        if stability >= 70:

            return "stable_evolution"


        return "needs_observation"



    def snapshot(self):

        return {

            "report_count":
                len(self.reports)

        }
