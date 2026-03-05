from mfdballm.execution.agent import BaseAgent
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.tools.schema_builder import build_tool_schema


class ToolAgent(BaseAgent):

    def __init__(self, router, tool_executor: ToolExecutor, registry, max_iterations: int = 5):
        self.router = router
        self.tool_executor = tool_executor
        self.registry = registry
        self.max_iterations = max_iterations

    async def run(self, messages):

        iteration = 0
        tools_schema = build_tool_schema(self.registry)

        while iteration < self.max_iterations:

            response = await self.router.chat(messages, tools=tools_schema)

            if not response.tool_calls:
                return response.text

            for call in response.tool_calls:

                result = await self.tool_executor.execute(
                    call.name,
                    call.arguments
                )

                messages.append({
                    "role": "tool",
                    "name": call.name,
                    "content": str(result)
                })

            iteration += 1

        return "Tool iteration limit reached"
