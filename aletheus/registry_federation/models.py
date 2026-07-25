"""
Registry Federation Models
"""


from dataclasses import dataclass


@dataclass
class EngineBinding:

    engine: str

    domain: str

    registries: list

    status: str = "pending"

