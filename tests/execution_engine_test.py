import asyncio

from mfdballm.execution.engine import ExecutionEngine
from mfdballm.execution.agent import BaseAgent


class TestAgent(BaseAgent):

    async def run(self, message: str):
        return message.upper()


async def main():

    agent = TestAgent()

    engine = ExecutionEngine(agent)

    result = await engine.run("hello")

    assert result.output == "HELLO"

    print("EXECUTION ENGINE TEST PASSED")


asyncio.run(main())
