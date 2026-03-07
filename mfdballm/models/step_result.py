from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from mfdballm.models.tool_call import ToolCall


@dataclass
class StepResult:

    step_index: int
    step_type: str

    input: Any = None
    output: Any = None

    tool_calls: List[ToolCall] = field(default_factory=list)
    tool_results: List[Any] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StepResult":

        tool_calls = [
            tc if isinstance(tc, ToolCall) else ToolCall(tc["name"], tc.get("arguments", {}))
            for tc in data.get("tool_calls", [])
        ]

        return cls(
            step_index=data["step_index"],
            step_type=data["step_type"],
            input=data.get("input"),
            output=data.get("output"),
            tool_calls=tool_calls,
            tool_results=data.get("tool_results", []),
            metadata=data.get("metadata", {}),
            error=data.get("error"),
        )
