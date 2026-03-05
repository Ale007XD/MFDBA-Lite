import json
from typing import Dict, Any, Callable


class ToolExecutor:
    """
    Executes tool calls safely.
    """

    def __init__(self, tools: Dict[str, Callable]):

        self.tools = tools

    def _normalize_arguments(self, arguments):

        # Already correct
        if isinstance(arguments, dict):
            return arguments

        # JSON string
        if isinstance(arguments, str):

            if arguments.strip() == "":
                return {}

            try:
                parsed = json.loads(arguments)

                if isinstance(parsed, dict):
                    return parsed

            except Exception:
                pass

        # fallback
        return {}

    def execute(self, tool_name: str, arguments: Dict[str, Any]):

        if tool_name not in self.tools:
            raise RuntimeError(f"Unknown tool: {tool_name}")

        tool = self.tools[tool_name]

        arguments = self._normalize_arguments(arguments)

        return tool(**arguments)
