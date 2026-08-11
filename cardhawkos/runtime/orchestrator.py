import time
import traceback
from datetime import datetime

from cardhawkos.runtime.logger import CardHawkLogger
from event_bus.runtime.bus import EventBus


class RuntimeOrchestrator:
    """
    CardHawkOS Runtime Orchestrator™

    Central execution layer for workflows, engine runs,
    event publishing, timing, and error handling.
    """

    @staticmethod
    def run_step(
        name,
        callback,
        event_type="runtime.step.completed",
        source="RuntimeOrchestrator",
        asset_id=None,
        payload=None,
    ):
        payload = payload or {}

        started = datetime.utcnow().isoformat()
        start_time = time.time()

        try:
            result = callback()

            duration = round(time.time() - start_time, 4)
            completed = datetime.utcnow().isoformat()

            EventBus.publish(
                event_type,
                source=source,
                asset_id=asset_id,
                title=f"{name} completed",
                message=f"{name} completed in {duration}s",
                payload={
                    "step": name,
                    "status": "SUCCESS",
                    "started": started,
                    "completed": completed,
                    "duration": duration,
                    "result": result,
                    **payload,
                },
            )

            CardHawkLogger.info(f"{name} completed in {duration}s")

            return {
                "step": name,
                "status": "SUCCESS",
                "started": started,
                "completed": completed,
                "duration": duration,
                "result": result,
            }

        except Exception as exc:
            duration = round(time.time() - start_time, 4)
            completed = datetime.utcnow().isoformat()
            error = str(exc)
            trace = traceback.format_exc()

            EventBus.publish(
                "runtime.step.failed",
                source=source,
                asset_id=asset_id,
                title=f"{name} failed",
                message=error,
                payload={
                    "step": name,
                    "status": "FAILED",
                    "started": started,
                    "completed": completed,
                    "duration": duration,
                    "error": error,
                    "traceback": trace,
                    **payload,
                },
            )

            CardHawkLogger.error(f"{name} failed: {error}")

            return {
                "step": name,
                "status": "FAILED",
                "started": started,
                "completed": completed,
                "duration": duration,
                "error": error,
            }

    @staticmethod
    def run_workflow(name, steps):
        results = []

        EventBus.publish(
            "runtime.workflow.started",
            source="RuntimeOrchestrator",
            title=f"{name} started",
            message=f"Workflow {name} started.",
            payload={"workflow": name},
        )

        for step_name, callback in steps:
            result = RuntimeOrchestrator.run_step(
                step_name,
                callback,
                source=name,
            )

            results.append(result)

            if result["status"] == "FAILED":
                break

        status = "SUCCESS"

        if any(result["status"] == "FAILED" for result in results):
            status = "FAILED"

        EventBus.publish(
            "runtime.workflow.completed",
            source="RuntimeOrchestrator",
            title=f"{name} completed",
            message=f"Workflow {name} completed with status {status}.",
            payload={
                "workflow": name,
                "status": status,
                "results": results,
            },
        )

        return {
            "workflow": name,
            "status": status,
            "results": results,
        }
