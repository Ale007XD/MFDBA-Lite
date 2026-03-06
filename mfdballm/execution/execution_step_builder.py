from typing import Any, Dict, List, Optional

from mfdballm.models.step_result import StepResult
from mfdballm.models.step_type import StepType


class ExecutionStepBuilder:

    def __init__(self):

        self.step_index = 0

    def llm_response(
        self,
        input: Any = None,
        output: Any = None,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):

        step = StepResult(
            step_index=self.step_index,
            step_type=StepType.LLM_RESPONSE,
            input=input,
            output=output,
            tool_calls=tool_calls or [],
            metadata=metadata or {},
        )

        self.step_index += 1

        return step

    def tool_execution(
        self,
        tool_calls: List[Dict[str, Any]],
        tool_results: List[Any],
        metadata: Optional[Dict[str, Any]] = None,
    ):

        step = StepResult(
            step_index=self.step_index,
            step_type=StepType.TOOL_EXECUTION,
            tool_calls=tool_calls,
            tool_results=tool_results,
            metadata=metadata or {},
        )

        self.step_index += 1

        return step

    def final_answer(
        self,
        output: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ):

        step = StepResult(
            step_index=self.step_index,
            step_type=StepType.FINAL_ANSWER,
            output=output,
            metadata=metadata or {},
        )

        self.step_index += 1

        return step

    def system(
        self,
        message: Any,
        metadata: Optional[Dict[str, Any]] = None,
    ):

        step = StepResult(
            step_index=self.step_index,
            step_type=StepType.SYSTEM,
            output=message,
            metadata=metadata or {},
        )

        self.step_index += 1

        return step
