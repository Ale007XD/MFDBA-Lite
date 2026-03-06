import asyncio

from mfdballm.execution.execution_engine import ExecutionEngine
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.tool_registry import ToolRegistry
from mfdballm.types import ProviderResponse


class DummyRouter:

    async def chat(self, messages):
        return ProviderResponse(text="done")


class DummyTool:

    async def run(self, arguments):
        return "ok"


async def main():

    registry = ToolRegistry()

    registry.register("dummy", DummyTool())

    executor = ToolExecutor(registry)

    router = DummyRouter()

    engine = ExecutionEngine(router, executor)

    result = await engine.run([{"role": "user", "content": "hi"}])

    assert result == "done"

    print("EXECUTION ENGINE TEST PASSED")


if __name__ == "__main__":
    asyncio.run(main())
