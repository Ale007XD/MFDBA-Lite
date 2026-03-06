from dataclasses import dataclass


@dataclass
class ToolResult:

    tool_name: str

    output: object

    success: bool

    execution_time_ms: int = 0

    error: str | None = None
