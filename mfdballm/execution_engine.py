from mfdballm.tool_call_parser import parse_tool_calls


class ExecutionEngine:

    def __init__(self, router, tool_executor):
        self.router = router
        self.tool_executor = tool_executor

    async def run(self, messages):

        provider_response = await self.router.complete(messages)

        tool_calls = parse_tool_calls(provider_response)

        if not tool_calls:
            return provider_response.content

        results = []

        for call in tool_calls:
            result = await self.tool_executor.execute(
                call.name,
                call.arguments
            )

            results.append(result)

        return results
