class BootConditions:
    """
    Runtime Boot Conditions™

    Determines whether boot phases should execute.
    """

    @staticmethod
    def should_run(runtime, phase):

        policy = getattr(runtime, "policy", None)

        if policy is None:
            return True

        return policy.evaluate(
            runtime,
            f"boot.phase.{phase}",
        )
