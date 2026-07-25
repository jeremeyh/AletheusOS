from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    policy:str
    passed:bool
    observed:float
    threshold:float
    message:str
