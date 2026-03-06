from mfdballm.execution.agent import BaseAgent
from mfdballm.execution.tool_executor import ToolExecutor
from mfdballm.types_tool import ToolCall
from mfdballm.types_tool_result import ToolResult


class ExecutionEngine:
    """
    Core runtime orchestrator.

    Responsibilities:
    - Run agent reasoning
    - Detect tool calls
    - Execute tools
    - Feed results back into the agent

    Agent performs reasoning only.
    Engine performs orchestration.
    """

    def __init__(
        self,
        agent: BaseAgent,
        tool_executor: ToolExecutor,
        max_tool_loops: int = 8
    ):
        self.agent = agent
        self.tool_executor = tool_executor
        self.max_tool_loops = max_tool_loops

    async def run(self, message: str):

        context = message
        loops = 0

        while True:

            if loops > self.max_tool_loops:
                raise RuntimeError("Tool loop limit exceeded")

            response = await self.agent.run(context)

            # If agent returns plain text — finish
            if not isinstance(response, ToolCall):
                return response

            tool_call: ToolCall = response

            tool_result: ToolResult = await self.tool_executor.execute(tool_call)

            context = tool_result.content

            loops += 1
