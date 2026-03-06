from dataclasses import dataclass
from typing import Any, Optional, Dict


@dataclass
class ToolResult:
    """
    Standard result returned by any tool execution.
    """

    tool_name: str

    output: Any

    success: bool

    execution_time_ms: Optional[int] = None

    error: Optional[str] = None

    metadata: Optional[Dict] = None
