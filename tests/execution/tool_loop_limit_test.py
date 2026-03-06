import asyncio

from mfdballm.execution.tool_agent import ToolAgent
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.registry import ToolRegistry
from mfdballm.tools.base import BaseTool
from mfdballm.types import ProviderResponse


class LoopTool(BaseTool):

    name = "loop"
    description = "returns loop"

    async def run(self, args):
        return "loop"


class LoopRouter:

    async def chat(self, messages, tools=None):

        from mfdballm.types_tool import ToolCall

        return ProviderResponse(
            text=None,
            tool_calls=[ToolCall(name="loop", arguments={})]
        )


async def main():

    registry = ToolRegistry()
    registry.register(LoopTool())

    executor = ToolExecutor(registry)

    agent = ToolAgent(LoopRouter(), executor, max_iterations=3)

    result = await agent.run([])

    assert result == "Tool iteration limit reached"

    print("TOOL LOOP LIMIT TEST PASSED")


asyncio.run(main())
