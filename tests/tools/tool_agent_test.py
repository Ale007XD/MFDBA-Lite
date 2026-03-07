import asyncio

from mfdballm.agents.tool_agent import ToolAgent
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.registry import ToolRegistry
from mfdballm.tools.base import BaseTool
from mfdballm.types import ProviderResponse


class EchoTool(BaseTool):

    name = "echo"
    description = "echo tool"

    async def run(self, args):
        return args["text"]


class FakeRouter:

    async def chat(self, messages, tools=None):

        from mfdballm.types_tool import ToolCall

        return ProviderResponse(
            text=None,
            tool_calls=[
                ToolCall(
                    name="echo",
                    arguments={"text": "hello"}
                )
            ]
        )


async def main():

    registry = ToolRegistry()
    registry.register(EchoTool())

    executor = ToolExecutor(registry)

    agent = ToolAgent(FakeRouter(), executor)

    r = await agent.run([])

    assert r == "hello"

    print("TOOL AGENT TEST PASSED")


asyncio.run(main())
