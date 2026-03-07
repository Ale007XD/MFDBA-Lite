import asyncio
import time

from mfdballm.execution.execution_engine import ExecutionEngine


class DummyRouter:

    def __init__(self):
        self.calls = 0

    async def chat(self, messages):

        self.calls += 1

        # first iteration → call tools
        if self.calls == 1:
            return {
                "output": "call tools",
                "tool_calls": [
                    {"name": "tool1", "arguments": {}},
                    {"name": "tool2", "arguments": {}},
                ],
            }

        # second iteration → final answer
        return {
            "output": "done",
            "tool_calls": []
        }


class DummyToolExecutor:

    async def execute(self, tool_call):

        await asyncio.sleep(0.2)

        return "ok"


async def run_test():

    router = DummyRouter()
    tool_executor = DummyToolExecutor()

    engine = ExecutionEngine(
        router=router,
        tool_executor=tool_executor,
        max_tool_loops=4
    )

    messages = [
        {"role": "user", "content": "test"}
    ]

    start = time.perf_counter()

    result = await engine.run(messages)

    elapsed = time.perf_counter() - start

    assert result == "done"

    # sequential would be ~0.4s
    assert elapsed < 0.35


def test_parallel_tool_execution():

    asyncio.run(run_test())
