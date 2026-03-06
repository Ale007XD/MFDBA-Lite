from mfdballm.execution.execution_step_builder import ExecutionStepBuilder
from mfdballm.execution.execution_trace import ExecutionTrace
from mfdballm.models.provider_response import ProviderResponse


class AgentLoop:

    def __init__(self, router, tool_executor, max_iterations: int = 16):

        self.router = router
        self.tool_executor = tool_executor
        self.max_iterations = max_iterations

    async def run(self, messages):

        builder = ExecutionStepBuilder()
        trace = ExecutionTrace()

        current_messages = list(messages)

        iteration = 0

        while True:

            iteration += 1

            if iteration > self.max_iterations:

                raise RuntimeError("AgentLoop exceeded max iterations")

            raw_response = await self.router.chat(current_messages)

            response = ProviderResponse.normalize(raw_response)

            step = builder.llm_response(
                input=current_messages,
                output=response.text,
                tool_calls=response.tool_calls
            )

            trace.add(step)

            if not response.tool_calls:

                final_step = builder.final_answer(
                    output=response.text
                )

                trace.add(final_step)

                return response.text

            tool_results = await self.tool_executor.execute(response.tool_calls)

            tool_step = builder.tool_execution(
                tool_calls=response.tool_calls,
                tool_results=tool_results
            )

            trace.add(tool_step)

            current_messages = tool_results
