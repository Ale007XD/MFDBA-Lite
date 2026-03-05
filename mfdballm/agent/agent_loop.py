class AgentLoop:

    def __init__(self, router, tools):

        self.router = router
        self.tools = tools

    async def run(self, messages):

        for _ in range(10):

            response = await self.router.generate(messages)

            tool_call = detect_tool_call(response.text)

            if not tool_call:
                return response.text

            result = execute_tool(tool_call)

            messages.append({
                "role": "tool",
                "content": result
            })
