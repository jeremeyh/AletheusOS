from asset_core.repository.asset_repository import AssetRepository
from decision_engine.runtime.engine import DecisionEngine
from event_bus.runtime.bus import EventBus
from intelligence.runtime.output_store import EngineOutputStore


class DEFJobs:
    @staticmethod
    def rescore_all():
        assets = AssetRepository.all(include_archived=False) or []

        count = 0

        for asset in assets:
            report = DecisionEngine.evaluate(asset)

            EngineOutputStore.save(
                asset_id=asset.get("id"),
                engine="DEF",
                score=report.get("final_score"),
                recommendation=report.get("recommendation"),
                payload=report,
            )

            AssetRepository.update(
                asset.get("id"),
                {
                    "q_def": report.get("qdef_score"),
                    "d_def": report.get("ddef_score"),
                    "recommendation": report.get("recommendation"),
                    "confidence": report.get("confidence"),
                    "strike_zone": report.get("final_score"),
                },
            )

            EventBus.publish(
                "def.scored",
                source="DEF",
                asset_id=asset.get("id"),
                title="DEF Score Updated",
                message=f"{asset.get('player')} scored {report.get('final_score')}",
                payload=report,
            )

            count += 1

        return count
