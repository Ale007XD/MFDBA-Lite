from typing import Dict
from mfdballm.tools.base import BaseTool


class ToolRegistry:
    """
    Registry storing tool objects.
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):

        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:

        if name not in self._tools:
            raise RuntimeError(f"Tool not found: {name}")

        return self._tools[name]

    def list(self):

        return list(self._tools.keys())
