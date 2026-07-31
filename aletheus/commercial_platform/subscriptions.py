"""
Subscription Engine

Genesis 13.45
"""


class SubscriptionEngine:
    def __init__(self):

        self.plans = {}

    def register(self, plan):

        self.plans[plan.plan_id] = plan
