"""
Memory Anchor Circuit

Genesis 8
"""


from .base import RuntimeAnchorCircuit



class MemoryAnchorCircuit(RuntimeAnchorCircuit):


    def attach(self):

        self.connected = True

        self.runtime.memory_anchor = self

        return self.status()


    def capabilities(self):

        return [
            "memory",
            "memory_mesh"
        ]
