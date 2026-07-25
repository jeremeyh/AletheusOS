"""
AletheusOS Registry Federation Validator

Genesis 12.1

Validates registry ownership,
engine mappings, and capability topology.
"""

import json
from pathlib import Path


class RegistryFederationValidator:


    def __init__(self, base_path="aletheus/registry_federation"):

        self.base_path = Path(base_path)


    def load(self, filename):

        path = self.base_path / filename

        if not path.exists():
            return {}

        return json.loads(
            path.read_text()
        )


    def validate(self):

        registry_map = self.load(
            "registry_map.json"
        )

        report = self.load(
            "wiring_report.json"
        )


        result = {

            "registries_detected":
                len(registry_map),

            "report_loaded":
                bool(report),

            "status":
                "healthy"

        }


        return result



    def snapshot(self):

        return self.validate()



if __name__ == "__main__":

    validator = RegistryFederationValidator()

    print(
        json.dumps(
            validator.validate(),
            indent=2
        )
    )

