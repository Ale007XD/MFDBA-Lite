from typing import Any, Dict, Optional

from pydantic import BaseModel


class ToolCall(BaseModel):
    """
    Represents a tool call requested by the LLM.
    """

    name: str
    arguments: Dict[str, Any] = {}
    id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolCall":
        return cls(
            name=data["name"],
            arguments=data.get("arguments", {}),
            id=data.get("id"),
        )
