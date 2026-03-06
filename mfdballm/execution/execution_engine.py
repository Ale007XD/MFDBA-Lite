from mfdballm.runtime.agent_loop import AgentLoop


class ExecutionEngine:

    def __init__(self, router, tool_executor):

        self.router = router
        self.tool_executor = tool_executor

    async def run(self, messages):

        loop = AgentLoop(
            router=self.router,
            tool_executor=self.tool_executor
        )

        return await loop.run(messages)
