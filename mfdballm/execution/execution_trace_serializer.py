import json
from typing import Any, Dict, List

from .execution_trace import ExecutionTrace
from .step_result import StepResult


def step_to_dict(step: StepResult) -> Dict[str, Any]:
    return {
        "step_type": step.step_type.value,
        "output": step.output,
        "tool_name": step.tool_name,
        "metadata": step.metadata,
    }


def trace_to_dict(trace: ExecutionTrace) -> Dict[str, Any]:
    return {
        "steps": [step_to_dict(step) for step in trace.steps]
    }


def trace_to_json(trace: ExecutionTrace) -> str:
    return json.dumps(trace_to_dict(trace), indent=2)


def dict_to_trace(data: Dict[str, Any]) -> ExecutionTrace:
    trace = ExecutionTrace()

    for step in data.get("steps", []):
        trace.add(
            StepResult(
                step_type=step["step_type"],
                output=step.get("output"),
                tool_name=step.get("tool_name"),
                metadata=step.get("metadata"),
            )
        )

    return trace
