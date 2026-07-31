"""Evolution-specific errors."""


class EvolutionError(RuntimeError):
    """Base repository-evolution failure."""


class PlanValidationError(EvolutionError):
    """Raised when an evolution plan is invalid."""


class PreconditionsFailed(EvolutionError):
    """Raised when repository state does not match plan preconditions."""
