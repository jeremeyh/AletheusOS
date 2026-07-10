from __future__ import annotations


def register_kernel_compatibility_commands(runtime):
    commands = runtime.commands
    kernel = runtime.kernel_v2

    def boot(payload=None):
        boot_result = kernel.boot(runtime)

        if not isinstance(boot_result, dict):
            boot_result = {
                "result": boot_result,
            }

        kernel_state = boot_result.get("kernel")

        if not isinstance(kernel_state, dict):
            kernel_state = {
                "result": kernel_state,
            }

        kernel_state.setdefault(
            "status",
            boot_result.get("status", "online"),
        )

        boot_result["kernel"] = kernel_state
        return boot_result

    def sync(payload=None):
        return kernel.sync_runtime(runtime)

    def publish(payload=None):
        payload = payload or {}

        routed = kernel.route_event(
            event_type=payload.get(
                "event_type",
                "kernel.event",
            ),
            source=payload.get(
                "source",
                "runtime",
            ),
            payload=payload.get("payload", {}),
        )

        if isinstance(routed, dict):
            routed.setdefault("status", "routed")

        return routed

    def snapshot(payload=None):
        return kernel.snapshot()

    commands.register(
        "kernel.boot",
        boot,
        replace=True,
    )

    commands.register(
        "kernel.sync",
        sync,
        replace=True,
    )

    commands.register(
        "kernel.publish",
        publish,
        replace=True,
    )

    commands.register(
        "kernel.snapshot",
        snapshot,
        replace=True,
    )
