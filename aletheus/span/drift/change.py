from dataclasses import dataclass

@dataclass(frozen=True)
class Change:
    metric:str
    previous:float
    current:float
    delta:float
    trend:str
