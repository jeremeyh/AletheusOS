from orchestrator.runtime.engine import IntelligenceOrchestrator


class OrchestratorJobs:
    """
    ORCHESTRATOR™ Jobs

    Background-friendly wrappers for pipeline execution.
    """

    @staticmethod
    def run_all_assets():
        return IntelligenceOrchestrator.run_all_assets()

    @staticmethod
    def run_asset(asset_id):
        return IntelligenceOrchestrator.run_asset_pipeline(asset_id)

