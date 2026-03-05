import asyncio

from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.registry import ToolRegistry
from mfdballm.tools.base import BaseTool


class EchoTool(BaseTool):

    name = "echo"
    description = "echo tool"

    async def run(self, args):
        return args["text"]


async def main():

    registry = ToolRegistry()

    registry.register(EchoTool())

    executor = ToolExecutor(registry)

    result = await executor.execute("echo", {"text": "hello"})

    assert result == "hello"

    print("TOOL EXECUTOR TEST PASSED")


asyncio.run(main())
