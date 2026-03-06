from typing import Any, Dict, Optional
from enum import Enum
import uuid
import time


class StepType(str, Enum):

    SYSTEM = "system"
    MODEL = "model"
    TOOL = "tool"
    FINAL = "final"


class StepResult:

    def __init__(
        self,
        step_type: StepType,
        output: Any = None,
        tool_name: Optional[str] = None,
        parent_step_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        step_id: Optional[str] = None,
        timestamp: Optional[float] = None,
    ):

        self.step_id = step_id or str(uuid.uuid4())

        self.step_type = step_type
        self.output = output
        self.tool_name = tool_name

        self.parent_step_id = parent_step_id

        self.timestamp = timestamp or time.time()

        self.metadata = metadata or {}

    def to_dict(self):

        return {
            "step_id": self.step_id,
            "step_type": self.step_type.value,
            "output": self.output,
            "tool_name": self.tool_name,
            "parent_step_id": self.parent_step_id,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            step_type=StepType(data["step_type"]),
            output=data.get("output"),
            tool_name=data.get("tool_name"),
            parent_step_id=data.get("parent_step_id"),
            metadata=data.get("metadata"),
            step_id=data.get("step_id"),
            timestamp=data.get("timestamp"),
        )
