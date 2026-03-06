import asyncio

from mfdballm.execution.execution_engine import ExecutionEngine
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.tool_registry import ToolRegistry
from mfdballm.types import ProviderResponse
from mfdballm.types_tool_call import ToolCall


class DummyRouter:

    async def chat(self, messages):

        if len(messages) == 1:

            return ProviderResponse(
                text="",
                tool_calls=[
                    ToolCall(
                        name="echo",
                        arguments={"text": "hello"}
                    )
                ]
            )

        return ProviderResponse(text="done")


class EchoTool:

    async def run(self, arguments):

        return arguments["text"]


async def main():

    registry = ToolRegistry()

    registry.register("echo", EchoTool())

    executor = ToolExecutor(registry)

    router = DummyRouter()

    engine = ExecutionEngine(router, executor)

    result = await engine.run([
        {"role": "user", "content": "hi"}
    ])

    assert result == "done"

    print("EXECUTION ENGINE TOOL LOOP TEST PASSED")


if __name__ == "__main__":
    asyncio.run(main())
