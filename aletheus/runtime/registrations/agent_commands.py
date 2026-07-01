"""
Agent Command Registration

Version 4.7.8
"""


def register_agent_commands(runtime):

    commands = runtime.commands

    commands.register(
        "agent.register",
        runtime._cmd_agent_register,
    )

    commands.register(
        "agent.bootstrap",
        runtime._cmd_agent_bootstrap,
    )

    commands.register(
        "agent.list",
        runtime._cmd_agent_list,
    )

    commands.register(
        "agent.task.assign",
        runtime._cmd_agent_task_assign,
    )

    commands.register(
        "agent.run",
        runtime._cmd_agent_run,
    )

    commands.register(
        "agent.orchestrate",
        runtime._cmd_agent_orchestrate,
    )

    commands.register(
        "agent.stats",
        runtime._cmd_agent_stats,
    )
