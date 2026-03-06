import asyncio
from mfdballm.runtime.events import ToolResultEvent


class ToolExecutionHandler:

    def __init__(self, tool_executor):
        self.tool_executor = tool_executor

    async def __call__(self, event, state):

        tasks = [
            self.tool_executor.execute(call.name, call.arguments)
            for call in event.calls
        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=True
        )

        normalized_results = []

        for r in results:
            if isinstance(r, Exception):
                normalized_results.append(
                    {"error": str(r)}
                )
            else:
                normalized_results.append(r)

        return ToolResultEvent(result=normalized_results)
