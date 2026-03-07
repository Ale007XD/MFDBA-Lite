import pytest

from mfdballm.execution.execution_engine import ExecutionEngine
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.tool_registry import ToolRegistry
from mfdballm.types import ProviderResponse


class MultiToolRouter:

    async def chat(self, messages):

        # имитируем LLM ответ с несколькими tool calls
        return ProviderResponse(
            text=None,
            tool_calls=[
                {"name": "tool_a", "arguments": {}},
                {"name": "tool_b", "arguments": {}},
            ]
        )


class ToolA:

    async def run(self, arguments):
        return "A"


class ToolB:

    async def run(self, arguments):
        return "B"


@pytest.mark.asyncio
async def test_multiple_tool_calls():

    registry = ToolRegistry()

    registry.register("tool_a", ToolA())
    registry.register("tool_b", ToolB())

    executor = ToolExecutor(registry)
    router = MultiToolRouter()

    engine = ExecutionEngine(router, executor)

    result = await engine.run([{"role": "user", "content": "run tools"}])

    # важно что engine не упал
    assert result is not None
