from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ToolCall:

    name: str

    arguments: Dict[str, Any]
