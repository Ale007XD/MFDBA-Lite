from .registry import ToolRegistry


class ToolExecutor:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def execute(self, name: str, args: dict):
        tool = self.registry.get(name)
        return await tool.run(**args)
