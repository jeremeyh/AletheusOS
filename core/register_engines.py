"""
Registers all CardHawk Engines
"""

from core.engine_registry import engine_registry

ENGINES = [

    "THORX",

    "Hawk A•Eye",

    "Continuous Scout",

    "Founder AI",

    "Portfolio Digital Twin",

    "Adaptive Intelligence",

    "Live Data",

    "Marketplace Intelligence",

    "Negotiation AI",

]

class PlaceholderEngine:

    def __init__(self,name):

        self.name=name

for name in ENGINES:

    engine_registry.register(

        name,

        PlaceholderEngine(name)

    )

print("Registered",len(ENGINES),"engines.")
