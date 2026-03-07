import json
from typing import Any, Dict

from .execution_trace import ExecutionTrace
from mfdballm.models.step_result import StepResult


def step_to_dict(step: StepResult) -> Dict[str, Any]:
    return {
        "step_index": step.step_index,
        "step_type": step.step_type,
        "input": step.input,
        "output": step.output,
        "error": step.error,
    }


def trace_to_dict(trace: ExecutionTrace) -> Dict[str, Any]:
    return {
        "steps": [step_to_dict(step) for step in trace.all()]
    }


def trace_to_json(trace: ExecutionTrace) -> str:
    return json.dumps(trace_to_dict(trace), indent=2)


def dict_to_trace(data: Dict[str, Any]) -> ExecutionTrace:
    trace = ExecutionTrace()

    for step_data in data.get("steps", []):
        step = StepResult.from_dict(step_data)
        trace.add(step)

    return trace
