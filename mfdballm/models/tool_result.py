from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ToolResult:
    """
    Canonical result of tool execution.

    Produced by ToolExecutor and consumed by AgentLoop / ExecutionEngine.
    """

    tool_name: str

    output: Any

    success: bool

    execution_time_ms: int = 0

    error: Optional[str] = None
