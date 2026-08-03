"""
AletheusOS Registry Federation Engine

Maps intelligence engines into
logical platform registries.
"""

import json
import os


class RegistryFederator:
    def __init__(self):

        self.bindings = []

    def load_map(self, path="aletheus/registry_federation/registry_map.json"):

        with open(path) as file:
            return json.load(file)

    def classify_engine(self, engine):

        name = engine.lower()

        if any(x in name for x in ["memory", "knowledge", "semantic"]):
            return "cognitive"

        if any(x in name for x in ["reason", "logic", "hypothesis"]):
            return "reasoning"

        if any(x in name for x in ["agent"]):
            return "agents"

        if any(x in name for x in ["capability"]):
            return "capability"

        if any(x in name for x in ["govern", "policy", "audit"]):
            return "governance"

        if any(x in name for x in ["discover"]):
            return "discovery"

        if any(x in name for x in ["runtime", "service"]):
            return "runtime"

        return "cognitive"

    def wire_engine(self, engine):

        mapping = self.load_map()

        domain = self.classify_engine(engine)

        binding = {
            "engine": engine,
            "domain": domain,
            "registries": mapping.get(domain, {}).get("registries", []),
            "status": "wired",
        }

        self.bindings.append(binding)

        return binding

    def report(self):

        return {"engines": len(self.bindings), "bindings": self.bindings}


def discover_engines():

    engines = []

    for root, dirs, files in os.walk("aletheus/intelligence"):
        for file in files:
            if file.endswith(".py") and "Engine" in file:
                engines.append(file.replace(".py", ""))

    return engines


if __name__ == "__main__":
    federation = RegistryFederator()

    engines = discover_engines()

    for engine in engines:
        federation.wire_engine(engine)

    with open("aletheus/registry_federation/wiring_report.json", "w") as file:
        json.dump(federation.report(), file, indent=4)

    print(f"Wired {len(engines)} engines")
