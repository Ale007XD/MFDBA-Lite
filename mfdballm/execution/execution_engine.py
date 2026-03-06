from mfdballm.execution.execution_state import ExecutionState
from mfdballm.parsers.action_parser import parse
from mfdballm.types_action import ActionType


class ExecutionEngine:

    def __init__(self, router, tool_executor, max_iterations=5):

        self.router = router
        self.tool_executor = tool_executor
        self.max_iterations = max_iterations

    async def run(self, messages):

        state = ExecutionState(messages)

        while state.iteration < self.max_iterations:

            state.increment()

            response = await self.router.chat(state.messages)

            action = parse(response)

            if action.type == ActionType.TOOL:

                for call in action.payload["calls"]:

                    # assistant tool call message
                    state.messages.append({
                        "role": "assistant",
                        "tool_call": {
                            "name": call.name,
                            "arguments": call.arguments
                        }
                    })

                    result = await self.tool_executor.execute(
                        call.name,
                        call.arguments
                    )

                    state.add_tool_result(result)

                    # tool result message
                    state.messages.append({
                        "role": "tool",
                        "name": result.tool_name,
                        "content": str(result.output)
                    })

            if action.type == ActionType.FINISH:

                return action.payload["answer"]

        return "max_iterations_reached"
