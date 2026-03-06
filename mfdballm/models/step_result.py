from dataclasses import dataclass, field
from typing import Any, Dict, List

from mfdballm.models.step_type import StepType


@dataclass
class StepResult:

    step_index: int
    step_type: StepType

    input: Any = None
    output: Any = None

    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    tool_results: List[Any] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
