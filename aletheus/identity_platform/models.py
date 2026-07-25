"""
Identity Platform Models

Genesis 13.44
"""

from dataclasses import dataclass, field


@dataclass
class Identity:


    identity_id: str

    identity_type: str

    name: str

    tenant_id: str

    capabilities: list = field(
        default_factory=list
    )



@dataclass
class Tenant:


    tenant_id: str

    name: str

    members: list = field(
        default_factory=list
    )

