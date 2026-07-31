"""
Mission Command Handlers

Genesis 7 Runtime Orchestration

Extracted from runtime/core.py.
"""

from aletheus.runtime.context import RuntimeContext


def mission_create(runtime, context: RuntimeContext):

    payload = context.payload

    mission = runtime.mission.create_mission(
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

    runtime.memory.remember(
        key="mission_created",
        value=mission.to_dict(),
        namespace="aletheus.mission",
        memory_type="episodic",
        tags=[
            "mission",
            "autonomous",
        ],
    )

    entity = runtime.knowledge.create_entity(
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


def mission_from_goal(runtime, context: RuntimeContext):

    payload = context.payload

    mission = runtime.mission.generate_mission_from_goal(
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

    runtime.memory.remember(
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


def mission_list(runtime, context: RuntimeContext):

    context.add_result(
        "missions",
        runtime.mission.list_missions(context.payload.get("status")),
    )

    return context


def mission_run(runtime, context: RuntimeContext):

    run = runtime.mission.run_mission(
        context.payload.get(
            "mission_id",
            "",
        )
    )

    runtime.memory.remember(
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


def mission_complete(runtime, context: RuntimeContext):

    result = runtime.mission.complete_mission(
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


def mission_task_complete(runtime, context: RuntimeContext):

    result = runtime.mission.complete_task(
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


def mission_history(runtime, context: RuntimeContext):

    context.add_result(
        "mission_history",
        runtime.mission.history(),
    )

    return context


def mission_stats(runtime, context: RuntimeContext):

    context.add_result(
        "mission_stats",
        runtime.mission.statistics(),
    )

    return context
