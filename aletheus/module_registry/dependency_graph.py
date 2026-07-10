"""
Module Dependency Graph

Post-Genesis 80.5
"""


class DependencyGraph:


    def __init__(self):

        self.graph = {}



    def connect(
        self,
        source,
        target
    ):

        self.graph.setdefault(
            source,
            []
        ).append(target)



    def analyze(self):

        return {

            "connections":
            self.graph,

            "status":
            "active"

        }

