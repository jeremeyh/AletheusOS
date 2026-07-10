"""
Genesis 8.59
Cognitive Dependency Graph Engine
"""


class CognitiveDependencyGraph:


    def __init__(self):

        self.edges=[]



    def connect(
        self,
        source,
        target
    ):

        self.edges.append(
            (
                source,
                target
            )
        )



    def snapshot(self):

        return {

            "dependencies":
                len(self.edges)

        }
