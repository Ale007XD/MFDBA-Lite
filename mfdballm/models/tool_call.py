from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ToolCall:
    """
    Represents a tool call requested by the LLM.
    """

    name: str
    arguments: Dict[str, Any]
