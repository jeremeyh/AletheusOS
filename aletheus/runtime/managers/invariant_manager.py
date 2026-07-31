"""
Invariant Manager

Genesis 7.5
"""


class InvariantManager:
    def __init__(self, runtime):
        self.runtime = runtime

    def check(self):

        return {"healthy": True, "violations": []}
