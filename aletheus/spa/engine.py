"""
AletheusOS Spectrum Platform Analyzer

Genesis 151
"""


from .architecture_analyzer import ArchitectureAnalyzer
from .dependency_analyzer import DependencyAnalyzer
from .runtime_analyzer import RuntimeAnalyzer
from .contract_validator import ContractValidator
from .intelligence_analyzer import IntelligenceAnalyzer
from .genesis_tracker import GenesisTracker
from .health_score import HealthScoreEngine
from .recommendation_engine import RecommendationEngine



class SpectrumPlatformAnalyzer:


    def __init__(self):

        self.architecture = ArchitectureAnalyzer()

        self.dependencies = DependencyAnalyzer()

        self.runtime = RuntimeAnalyzer()

        self.contracts = ContractValidator()

        self.intelligence = IntelligenceAnalyzer()

        self.genesis = GenesisTracker()

        self.health = HealthScoreEngine()

        self.recommendations = RecommendationEngine()



    def initialize(self):

        return {

            "system":

            "spectrum_platform_analyzer",

            "genesis":

            "151",

            "status":

            "operational"

        }



    def full_scan(self):

        results = {


            "architecture":
            self.architecture.analyze(),


            "dependencies":
            self.dependencies.analyze(),


            "runtime":
            self.runtime.analyze(),


            "contracts":
            self.contracts.validate(),


            "intelligence":
            self.intelligence.analyze(),


            "genesis":
            self.genesis.analyze()

        }


        results["health"] = self.health.calculate(results)

        results["recommendations"] = self.recommendations.generate()


        return results

