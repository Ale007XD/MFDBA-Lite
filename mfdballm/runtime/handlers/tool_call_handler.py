import asyncio

from mfdballm.runtime.events import ToolResultEvent


class ToolCallHandler:

    def __init__(self, tool_executor):
        self.tool_executor = tool_executor

    async def handle(self, event, state):

        tasks = [
            self.tool_executor.execute(call.name, call.arguments)
            for call in event.tool_calls
        ]

        results = await asyncio.gather(*tasks)

        return ToolResultEvent(results)
