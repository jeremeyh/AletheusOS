"""
Governance Audit Memory

Genesis 13.54
"""


class GovernanceAudit:
    def __init__(self):

        self.records = []

    def record(self, decision):

        self.records.append(decision)
