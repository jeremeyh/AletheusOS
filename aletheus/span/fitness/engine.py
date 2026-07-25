from .function import FitnessFunction
from .result import FitnessResult


class FitnessEngine:
    def __init__(self):
        self.functions=[]

    def register(self,f:FitnessFunction):
        self.functions.append(f)

    @classmethod
    def default(cls):
        e=cls()
        e.register(FitnessFunction("Limit Fan-Out","fan_out",25,"min"))
        e.register(FitnessFunction("Limit Fan-In","fan_in",40,"min"))
        return e

    def evaluate(self,metrics:dict):
        results=[]
        for f in self.functions:
            observed=metrics.get(f.metric,0)
            passed=observed<=f.target if f.direction=="min" else observed>=f.target
            score=100.0 if passed else max(0.0,100-((observed-f.target)*2))
            results.append(FitnessResult(f.name,round(score,2),passed,observed,f.target))
        return results
