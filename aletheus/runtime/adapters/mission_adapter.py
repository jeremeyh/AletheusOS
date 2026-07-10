"""
Mission Command Adapter

Genesis 7

Extracted from runtime/core.py

Owns mission command execution boundary.
"""


class MissionCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime


    def create(self, context):

        payload = context.payload

        mission = self.runtime.mission.create_mission(
            title=payload.get(
                "title",
                "Untitled Mission",
            ),
            objective=payload.get(
                "objective",
                "",
            ),
            application=payload.get(
                "application",
                context.application,
            ),
            priority=payload.get(
                "priority",
                "medium",
            ),
            tasks=payload.get(
                "tasks",
                [],
            ),
        )

        self.runtime.memory.remember(
            key="mission_created",
            value=mission.to_dict(),
            namespace="aletheus.mission",
            memory_type="episodic",
            tags=[
                "mission",
                "autonomous",
            ],
        )

        entity = self.runtime.knowledge.create_entity(
            label=mission.title,
            entity_type="mission",
            properties={
                "mission_id": mission.mission_id,
                "objective": mission.objective,
            },
        )

        context.add_result(
            "mission",
            mission.to_dict(),
        )

        context.add_result(
            "knowledge_entity",
            entity.to_dict(),
        )

        return context


    def from_goal(self, context):

        payload = context.payload

        mission = self.runtime.mission.generate_mission_from_goal(
            goal_title=payload.get(
                "goal_title",
                payload.get(
                    "title",
                    "Untitled Goal",
                ),
            ),
            goal_description=payload.get(
                "goal_description",
                payload.get(
                    "description",
                    "",
                ),
            ),
            application=payload.get(
                "application",
                context.application,
            ),
            priority=payload.get(
                "priority",
                "high",
            ),
        )

        self.runtime.memory.remember(
            key="mission_generated_from_goal",
            value=mission.to_dict(),
            namespace="aletheus.mission",
            memory_type="episodic",
            tags=[
                "mission",
                "goal",
                "autonomous",
            ],
        )

        context.add_result(
            "mission",
            mission.to_dict(),
        )

        return context


    def list(self, context):

        context.add_result(
            "missions",
            self.runtime.mission.list_missions(
                context.payload.get(
                    "status"
                )
            ),
        )

        return context


    def run(self, context):

        run = self.runtime.mission.run_mission(
            context.payload.get(
                "mission_id",
                "",
            )
        )

        self.runtime.memory.remember(
            key="mission_run",
            value=run.to_dict(),
            namespace="aletheus.mission",
            memory_type="decision",
            tags=[
                "mission",
                "run",
                "autonomous",
            ],
        )

        context.add_result(
            "mission_run",
            run.to_dict(),
        )

        return context


    def complete(self, context):

        result = self.runtime.mission.complete_mission(
            context.payload.get(
                "mission_id",
                "",
            )
        )

        context.add_result(
            "mission",
            result,
        )

        return context


    def task_complete(self, context):

        result = self.runtime.mission.complete_task(
            mission_id=context.payload.get(
                "mission_id",
                "",
            ),
            task_id=context.payload.get(
                "task_id",
                "",
            ),
        )

        context.add_result(
            "mission",
            result,
        )

        return context


    def history(self, context):

        context.add_result(
            "mission_history",
            self.runtime.mission.history(),
        )

        return context


    def stats(self, context):

        if hasattr(
            self.runtime.mission,
            "stats",
        ):
            result = self.runtime.mission.stats()

        elif hasattr(
            self.runtime.mission,
            "statistics",
        ):
            result = self.runtime.mission.statistics()

        else:
            result = {
                "status": "unknown"
            }

        context.add_result(
            "mission_stats",
            result,
        )

        return context
