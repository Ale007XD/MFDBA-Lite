from typing import Any, Dict

from mfdballm.tools.registry import ToolRegistry


class ToolExecutor:
    """
    Deterministic execution layer for tools.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def execute(self, tool_name: str, args: Dict[str, Any]):

        tool = self.registry.get(tool_name)

        result = await tool.run(args)

        return result
