from typing import List, Dict, Optional
from mfdballm.models.step_result import StepResult


class ExecutionTrace:

    def __init__(self):

        self.steps: List[StepResult] = []

        self._index: Dict[int, StepResult] = {}

    def add(self, step: StepResult):

        self.steps.append(step)

        if step.step_index is not None:
            self._index[step.step_index] = step

    def last(self) -> Optional[StepResult]:

        if not self.steps:
            return None

        return self.steps[-1]

    def get(self, step_index: int) -> Optional[StepResult]:

        return self._index.get(step_index)

    def children(self, step_index: int) -> List[StepResult]:

        result = []

        for step in self.steps:
            if step.parent_step_index == step_index:
                result.append(step)

        return result

    def roots(self) -> List[StepResult]:

        result = []

        for step in self.steps:
            if step.parent_step_index is None:
                result.append(step)

        return result

    def to_dict(self):

        return {
            "steps": [step.to_dict() for step in self.steps]
        }

    @classmethod
    def from_dict(cls, data):

        trace = cls()

        for step_data in data["steps"]:
            step = StepResult.from_dict(step_data)
            trace.add(step)

        return trace
