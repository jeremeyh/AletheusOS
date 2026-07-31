"""
Runtime Anchor Registry

Genesis 8.2

Owns lifecycle and discovery of runtime anchor circuits.
"""


class AnchorRegistry:
    def __init__(self, runtime):

        self.runtime = runtime
        self.anchors = {}

    def register(self, name, anchor):

        self.anchors[name] = anchor

        return anchor.status()

    def attach_all(self):

        results = {}

        for name, anchor in self.anchors.items():
            results[name] = anchor.attach()

        return results

    def get(self, name):

        return self.anchors.get(name)

    def list(self):

        return sorted(self.anchors.keys())

    def validate_contracts(self):

        return {
            name: anchor.validate_contract() for name, anchor in self.anchors.items()
        }

    def status(self):

        return {
            "count": len(self.anchors),
            "anchors": {name: anchor.status() for name, anchor in self.anchors.items()},
            "healthy": all(anchor.connected for anchor in self.anchors.values()),
        }
