from mfdballm.execution.execution_state import ExecutionState
from mfdballm.parsers.action_parser import parse_provider_response
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

            action = parse_provider_response(response)

            if action.type == ActionType.TOOL:

                for call in action.payload['calls']:

                    result = await self.tool_executor.execute(
                        call.name,
                        call.arguments
                    )

                    state.add_tool_result(result)

            if action.type == ActionType.FINISH:

                return action.payload['answer']

        return 'max_iterations_reached'
