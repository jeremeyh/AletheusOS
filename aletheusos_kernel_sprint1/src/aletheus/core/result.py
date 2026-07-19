from dataclasses import dataclass,field
from typing import Generic,TypeVar
T=TypeVar("T")
@dataclass(frozen=True,slots=True)
class Result(Generic[T]):
    success:bool
    message:str
    value:T|None=None
    diagnostics:tuple[str,...]=field(default_factory=tuple)
    @classmethod
    def ok(cls,value=None,message="Success"):
        return cls(True,message,value)
    @classmethod
    def fail(cls,message,diagnostics=()):
        return cls(False,message,None,diagnostics)
