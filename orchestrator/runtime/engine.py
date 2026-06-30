from datetime import datetime
import time

from asset_core.repository.asset_repository import AssetRepository
from decision_engine.runtime.engine import DecisionEngine
from event_bus.runtime.bus import EventBus
from falcon.runtime.engine import FalconEngine
from intelligence.runtime.output_store import EngineOutputStore
from marketplace.runtime.market_snapshot import MarketSnapshot
from nest.runtime.score import NestScoringEngine
from orchestrator.models.context import PipelineContext
from orchestrator.runtime.execution_log import OrchestratorExecutionLog


class IntelligenceOrchestrator:
    """
    ORCHESTRATOR™

    Coordinates asset intelligence workflows across:
    Marketplace → THORᵡ → DEF → NEST → FALCON → Persistence → Events.
    """

    @staticmethod
    def _run_step(context, name, callback):
        start = time.time()

        try:
            result = callback()
            duration = round(time.time() - start, 4)

            context.add_event(
                name,
                {
                    "status": "SUCCESS",
                    "duration": duration,
                },
            )

            context.set_metric(
                f"{name.lower().replace(' ', '_')}_duration",
                duration,
            )

            EventBus.publish(
                "orchestrator.step.completed",
                source="ORCHESTRATOR",
                asset_id=context.asset_id,
                title=f"{name} completed",
                message=f"{name} completed in {duration}s.",
                payload={
                    "step": name,
                    "duration": duration,
                },
            )

            return result

        except Exception as exc:
            duration = round(time.time() - start, 4)

            context.add_error(name, exc)

            EventBus.publish(
                "orchestrator.step.failed",
                source="ORCHESTRATOR",
                asset_id=context.asset_id,
                title=f"{name} failed",
                message=str(exc),
                payload={
                    "step": name,
                    "duration": duration,
                    "error": str(exc),
                },
            )

            return None

    @staticmethod
    def run_asset_pipeline(asset_id):
        start = time.time()

        context = PipelineContext(
            asset_id=asset_id,
        )

        asset = AssetRepository.get(asset_id)

        if not asset:
            context.add_error(
                "Load Asset",
                f"Asset {asset_id} not found.",
            )

            OrchestratorExecutionLog.record(
                context,
                status="FAILED",
                duration=0,
            )

            return context.to_dict()

        context.asset = asset

        context.add_event(
            "Asset Loaded",
            {
                "player": asset.get("player"),
            },
        )

        market = IntelligenceOrchestrator._run_step(
            context,
            "Marketplace Intelligence",
            lambda: MarketSnapshot.build(asset),
        )

        if market:
            context.market = market

            AssetRepository.update_market(
                asset_id,
                market,
            )

            EngineOutputStore.save(
                asset_id=asset_id,
                engine="Marketplace",
                score=market.get("confidence", 0),
                recommendation=market.get("market_velocity", ""),
                payload=market,
            )

        updated_asset = AssetRepository.get(asset_id) or asset

        def_report = IntelligenceOrchestrator._run_step(
            context,
            "DEF",
            lambda: DecisionEngine.evaluate(updated_asset),
        )

        if def_report:
            context.def_report = def_report

            AssetRepository.update(
                asset_id,
                {
                    "q_def": def_report.get("qdef_score"),
                    "d_def": def_report.get("ddef_score"),
                    "recommendation": def_report.get("recommendation"),
                    "confidence": def_report.get("confidence"),
                },
            )

            EngineOutputStore.save(
                asset_id=asset_id,
                engine="DEF",
                score=def_report.get("final_score"),
                recommendation=def_report.get("recommendation"),
                payload=def_report,
            )

        updated_asset = AssetRepository.get(asset_id) or updated_asset

        nest = IntelligenceOrchestrator._run_step(
            context,
            "NEST",
            lambda: NestScoringEngine.calculate(updated_asset),
        )

        if nest:
            context.nest = {
                "score": nest.score,
                "grade": nest.grade,
                "recommendation": nest.recommendation,
                "confidence": nest.confidence,
            }

            EngineOutputStore.save(
                asset_id=asset_id,
                engine="NEST",
                score=nest.score,
                recommendation=nest.recommendation,
                payload=context.nest,
            )

        falcon = IntelligenceOrchestrator._run_step(
            context,
            "FALCON Snapshot",
            lambda: FalconEngine.record_snapshot(),
        )

        if falcon:
            context.falcon = falcon

            EngineOutputStore.save(
                asset_id=asset_id,
                engine="FALCON",
                score=falcon.get("average_nest", 0),
                recommendation="Snapshot Recorded",
                payload=falcon,
            )

        duration = round(time.time() - start, 4)
        context.completed_at = datetime.utcnow().isoformat()
        context.set_metric("total_duration", duration)

        status = "SUCCESS"

        if context.errors:
            status = "PARTIAL"

        run_id = OrchestratorExecutionLog.record(
            context,
            status=status,
            duration=duration,
        )

        EventBus.publish(
            "orchestrator.pipeline.completed",
            source="ORCHESTRATOR",
            asset_id=asset_id,
            title="Asset Intelligence Pipeline Completed",
            message=f"Pipeline completed for asset {asset_id} with status {status}.",
            payload={
                "run_id": run_id,
                "status": status,
                "duration": duration,
                "errors": context.errors,
            },
        )

        return context.to_dict()

    @staticmethod
    def run_all_assets():
        assets = AssetRepository.all(include_archived=False) or []

        results = []

        for asset in assets:
            result = IntelligenceOrchestrator.run_asset_pipeline(
                asset.get("id"),
            )

            results.append(result)

        return results
