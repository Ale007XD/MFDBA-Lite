from mfdballm.execution.execution_engine import ExecutionEngine
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.tool_registry import ToolRegistry


class ToolAgent:

    def __init__(
        self,
        router,
        tool_executor=None,
        registry=None,
        max_iterations: int = 16
    ):

        if tool_executor is None:

            if registry is None:
                registry = ToolRegistry()

            tool_executor = ToolExecutor(registry)

        self.engine = ExecutionEngine(
            router=router,
            tool_executor=tool_executor,
            max_iterations=max_iterations
        )

    async def run(self, messages):

        return await self.engine.run(messages)
