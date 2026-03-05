from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ToolCall:
    """
    Standard representation of a tool invocation produced by an LLM.
    """

    name: str
    arguments: Dict[str, Any]
