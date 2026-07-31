from __future__ import annotations


class CapabilityStatistics:
    GENESIS = "21.6"
    VERSION = "1.0.0"

    def __init__(self):
        self.reset()

    def reset(self):
        self.evaluations = 0
        self.approvals = 0
        self.denials = 0
        self.grants = 0
        self.revocations = 0

    def record_decision(self, approved: bool):

        self.evaluations += 1

        if approved:
            self.approvals += 1
        else:
            self.denials += 1

    def record_grant(self):
        self.grants += 1

    def record_revocation(self):
        self.revocations += 1

    def snapshot(self):

        return {
            "evaluations": self.evaluations,
            "approvals": self.approvals,
            "denials": self.denials,
            "grants": self.grants,
            "revocations": self.revocations,
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }

    def health(self):

        return {
            "status": "healthy",
            **self.snapshot(),
        }


capability_statistics = CapabilityStatistics()
