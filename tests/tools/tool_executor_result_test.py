import asyncio

from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.registry import ToolRegistry
from mfdballm.tools.base import BaseTool


class EchoTool(BaseTool):

    name = 'echo'
    description = 'echo'

    async def run(self, args):
        return args['text']


async def main():

    registry = ToolRegistry()
    registry.register(EchoTool())

    executor = ToolExecutor(registry)

    r = await executor.execute('echo', {'text': 'hello'})

    assert r.output == 'hello'
    assert r.success is True

    print('TOOL EXECUTOR RESULT TEST PASSED')


asyncio.run(main())
