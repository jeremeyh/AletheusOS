"""
Workflow v2 Command Registration

Genesis 6
"""

def register_workflow_v2_commands(runtime):

    commands = runtime.commands

    commands.register(
        "workflow.v2.create",
        runtime._cmd_workflow_v2_create,
    )

    commands.register(
        "workflow.v2.execute_next",
        runtime._cmd_workflow_v2_execute_next,
    )

    commands.register(
        "workflow.v2.execute",
        runtime._cmd_workflow_v2_execute,
    )

    commands.register(
        "workflow.v2.pause",
        runtime._cmd_workflow_v2_pause,
    )

    commands.register(
        "workflow.v2.resume",
        runtime._cmd_workflow_v2_resume,
    )

    commands.register(
        "workflow.v2.cancel",
        runtime._cmd_workflow_v2_cancel,
    )

    commands.register(
        "workflow.v2.list",
        runtime._cmd_workflow_v2_list,
    )

    commands.register(
        "workflow.v2.history",
        runtime._cmd_workflow_v2_history,
    )

    commands.register(
        "workflow.v2.stats",
        runtime._cmd_workflow_v2_stats,
    )
