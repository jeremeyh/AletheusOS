"""
Commercial Platform Models

Genesis 13.45
"""

from dataclasses import dataclass, field


@dataclass
class SubscriptionPlan:


    plan_id: str

    name: str

    capabilities: list = field(
        default_factory=list
    )



@dataclass
class CustomerSubscription:


    customer_id: str

    plan_id: str

    status: str = "active"

