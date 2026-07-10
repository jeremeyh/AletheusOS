"""
SPA Anchor Governance Analyzer

Genesis 8.4

Analyzes Runtime Anchor Circuit health,
contracts, and expansion risk.
"""


class AnchorGovernanceAnalyzer:


    def __init__(self, runtime):

        self.runtime = runtime



    def analyze(self):

        registry = getattr(
            self.runtime,
            "anchor_registry",
            None
        )


        if registry is None:

            return {

                "status": "unavailable",
                "risk_count": 1,
                "risks": [
                    "Anchor registry missing"
                ]

            }



        contracts = (
            registry.validate_contracts()
        )


        violations = [

            name

            for name, result
            in contracts.items()

            if not result.get(
                "valid",
                False
            )

        ]


        return {

            "status":
                "healthy"
                if not violations
                else "warning",

            "anchor_count":
                len(registry.list()),

            "contract_violations":
                len(violations),

            "risks":
                violations,

            "drift_detected":
                len(violations) > 0

        }
