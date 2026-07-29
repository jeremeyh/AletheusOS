def _cmd_goal_list(
    self,
    context: RuntimeContext,
) -> RuntimeContext:
    """
    Return goals matching the requested status.
    """

    context.add_result(
        "goals",
        self.cognition.list_goals(
            context.payload.get("status"),
        ),
    )

    return context
