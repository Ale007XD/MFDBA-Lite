import pytest

from mfdballm.execution.execution_engine import ExecutionEngine
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.tool_registry import ToolRegistry
from mfdballm.types import ProviderResponse


class DummyRouter:

    async def chat(self, messages):
        return ProviderResponse(text="done")


class FailingTool:

    async def run(self, arguments):
        raise RuntimeError("tool failure")


@pytest.mark.asyncio
async def test_tool_exception_handling():

    registry = ToolRegistry()
    registry.register("fail", FailingTool())

    executor = ToolExecutor(registry)
    router = DummyRouter()

    engine = ExecutionEngine(router, executor)

    result = await engine.run([{"role": "user", "content": "hi"}])

    # engine должен пережить падение tool
    assert result == "done"
