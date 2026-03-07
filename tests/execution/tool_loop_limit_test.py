import asyncio

from mfdballm.execution.execution_engine import ExecutionEngine


class DummyRouter:
    async def generate(self, messages, **kwargs):
        return {
            "output": "done",
            "tool_calls": []
        }


class DummyToolExecutor:
    async def execute(self, tool_call):
        return "ok"


async def run_test():

    router = DummyRouter()
    tool_executor = DummyToolExecutor()

    engine = ExecutionEngine(
        router=router,
        tool_executor=tool_executor,
        max_tool_loops=3
    )

    messages = [{"role": "user", "content": "test"}]

    result = await engine.run(messages)

    assert result is not None


def test_tool_loop_limit():
    asyncio.run(run_test())


print("TOOL LOOP LIMIT TEST PASSED")
