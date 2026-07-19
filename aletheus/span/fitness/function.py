from dataclasses import dataclass

@dataclass(frozen=True)
class FitnessFunction:
    name:str
    metric:str
    target:float
    direction:str="max"   # max|min
