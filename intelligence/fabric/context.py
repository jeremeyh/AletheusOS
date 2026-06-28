"""
CardHawk OS™
Execution Context
"""

import uuid


class ExecutionContext:

    def __init__(self):

        self.correlation_id = str(uuid.uuid4())

        self.causation_id = None

        self.asset_id = None

        self.user = "Founder"

    def child(self):

        ctx = ExecutionContext()

        ctx.correlation_id = self.correlation_id

        ctx.causation_id = self.correlation_id

        ctx.asset_id = self.asset_id

        ctx.user = self.user

        return ctx


context = ExecutionContext()
