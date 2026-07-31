"""
Governance Manager

Genesis 7.2
"""


class GovernanceManager:
    def __init__(self, runtime):
        self.runtime = runtime

    def status(self):

        return {"compliant": True, "violations": []}
