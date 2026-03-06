import asyncio

from mfdballm.execution.engine import ExecutionEngine
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.execution.agent import BaseAgent


class DummyAgent(BaseAgent):

    async def run(self, message: str):
        return "Hello from agent!"


async def main():

    tools = {}
    tool_executor = ToolExecutor(tools)

    agent = DummyAgent()

    engine = ExecutionEngine(
        agent=agent,
        tool_executor=tool_executor
    )

    result = await engine.run("Hello")

    print("\nENGINE RESULT:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
