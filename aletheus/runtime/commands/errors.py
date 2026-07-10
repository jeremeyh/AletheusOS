from __future__ import annotations


class CommandDispatchError(RuntimeError):
    """Base error for command dispatch failures."""


class CommandNotFoundError(CommandDispatchError):
    def __init__(self, command_name: str) -> None:
        super().__init__(f"Command is not registered: {command_name!r}")
        self.command_name = command_name


class DuplicateCommandError(CommandDispatchError):
    def __init__(self, command_name: str) -> None:
        super().__init__(f"Duplicate command registration: {command_name!r}")
        self.command_name = command_name


class RegistryFrozenError(CommandDispatchError):
    def __init__(self) -> None:
        super().__init__("The command registry is immutable after construction.")


class CommandValidationError(CommandDispatchError):
    def __init__(self, command_name: str, message: str) -> None:
        super().__init__(f"Invalid request for {command_name!r}: {message}")
        self.command_name = command_name


class CommandResultTypeError(CommandDispatchError):
    def __init__(
        self,
        command_name: str,
        expected: type,
        actual: type,
    ) -> None:
        super().__init__(
            f"Invalid result for {command_name!r}: "
            f"expected {expected.__qualname__}, got {actual.__qualname__}"
        )
        self.command_name = command_name
        self.expected = expected
        self.actual = actual


class CommandExecutionError(CommandDispatchError):
    def __init__(self, command_name: str, cause: BaseException) -> None:
        super().__init__(f"Command execution failed for {command_name!r}: {cause}")
        self.command_name = command_name
        self.__cause__ = cause
