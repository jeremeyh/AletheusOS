"""
Kernel Command Registration

Genesis 6
"""

def register_kernel_commands(runtime):

    commands = runtime.commands

    commands.register(
        "kernel.boot",
        runtime._cmd_kernel_boot,
    )

    commands.register(
        "kernel.status",
        runtime._cmd_kernel_status,
    )

    commands.register(
        "kernel.sync",
        runtime._cmd_kernel_sync,
    )

    commands.register(
        "kernel.publish",
        runtime._cmd_kernel_publish,
    )

    commands.register(
        "kernel.snapshot",
        runtime._cmd_kernel_snapshot,
    )

    commands.register(
        "kernel.stats",
        runtime._cmd_kernel_stats,
    )

    commands.register(
        "kernel.bootstrap",
        runtime._cmd_kernel_bootstrap,
    )

    commands.register(
        "kernel.execute",
        runtime._cmd_kernel_execute,
    )

    commands.register(
        "kernel.tasks",
        runtime._cmd_kernel_tasks,
    )

    commands.register(
        "kernel.scheduler",
        runtime._cmd_kernel_scheduler,
    )

    commands.register(
        "kernel.dispatcher",
        runtime._cmd_kernel_dispatcher,
    )

    commands.register(
        "kernel.supervisor",
        runtime._cmd_kernel_supervisor,
    )

    commands.register(
        "kernel.statistics",
        runtime._cmd_kernel_statistics,
    )
