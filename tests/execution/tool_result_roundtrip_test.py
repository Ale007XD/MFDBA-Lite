import asyncio

from mfdballm.execution.execution_engine import ExecutionEngine


class DummyRouter:

    def __init__(self):
        self.calls = 0

    async def chat(self, messages):

        self.calls += 1

        # first call → ask for tool
        if self.calls == 1:

            return {
                "output": "need tool",
                "tool_calls": [
                    {"name": "echo", "arguments": {"value": "hello"}}
                ]
            }

        # second call → verify tool result was returned
        last_message = messages[-1]

        assert last_message["role"] == "tool"
        assert last_message["content"] == "hello"

        return {
            "output": "tool worked",
            "tool_calls": []
        }


class DummyToolExecutor:

    async def execute(self, tool_call):

        return tool_call["arguments"]["value"]


async def run_test():

    router = DummyRouter()
    tool_executor = DummyToolExecutor()

    engine = ExecutionEngine(
        router=router,
        tool_executor=tool_executor
    )

    messages = [
        {"role": "user", "content": "test"}
    ]

    result = await engine.run(messages)

    assert result == "tool worked"


def test_tool_result_roundtrip():

    asyncio.run(run_test())
