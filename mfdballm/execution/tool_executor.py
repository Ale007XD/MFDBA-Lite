import time

from mfdballm.types_tool_result import ToolResult


class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    async def execute(self, tool_name, arguments):

        tool = self.registry.get(tool_name)

        start = time.time()

        try:

            result = await tool.run(arguments)

            elapsed = int((time.time() - start) * 1000)

            return ToolResult(
                tool_name=tool_name,
                output=result,
                success=True,
                execution_time_ms=elapsed
            )

        except Exception as e:

            elapsed = int((time.time() - start) * 1000)

            return ToolResult(
                tool_name=tool_name,
                output=None,
                success=False,
                execution_time_ms=elapsed,
                error=str(e)
            )
