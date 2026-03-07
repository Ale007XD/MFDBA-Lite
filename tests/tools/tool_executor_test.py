import asyncio

from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.registry import ToolRegistry
from mfdballm.models.tool_call import ToolCall


class EchoTool:

    name = "echo"

    async def run(self, **kwargs):
        return kwargs.get("text")


async def main():

    registry = ToolRegistry()
    registry.register(EchoTool())

    executor = ToolExecutor(registry)

    call = ToolCall(
        name="echo",
        arguments={"text": "hello"}
    )

    result = await executor.execute(call)

    assert result.success is True
    assert result.output == "hello"
    assert result.tool_name == "echo"

    print("TOOL EXECUTOR TEST PASSED")


if __name__ == "__main__":
    asyncio.run(main())
