from adaptive_intelligence.feedback.feedback_loop import IntelligenceFeedbackLoop
from adaptive_intelligence.explainability.explainer import IntelligenceExplainer
from adaptive_intelligence.simulation.simulation_lab import PortfolioSimulationLab
from adaptive_intelligence.quality.quality_dashboard import IntelligenceQualityDashboard
from adaptive_intelligence.research.research_workspace import ResearchWorkspace
from adaptive_intelligence.plugins.plugin_framework import PluginRegistry
from adaptive_intelligence.deployment.deployment_profiles import DeploymentProfiles
from adaptive_intelligence.governance.platform_governance import PlatformGovernance

class AdaptiveIntelligenceService:
    """Facade for CardHawk OS™ 7.0 Adaptive Intelligence."""

    feedback = IntelligenceFeedbackLoop
    explainer = IntelligenceExplainer
    simulation = PortfolioSimulationLab
    quality = IntelligenceQualityDashboard
    research = ResearchWorkspace
    plugins = PluginRegistry
    deployment = DeploymentProfiles
    governance = PlatformGovernance

    @staticmethod
    def dashboard():
        return {
            "quality": IntelligenceQualityDashboard.snapshot(),
            "plugins": [p.__dict__ for p in PluginRegistry.seed_defaults()],
            "deployment_profiles": DeploymentProfiles.all(),
            "governance": PlatformGovernance.validate(),
        }
