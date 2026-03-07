import asyncio

from mfdballm.execution.execution_step_builder import ExecutionStepBuilder
from mfdballm.execution.execution_trace import ExecutionTrace
from mfdballm.models.provider_response import ProviderResponse
from mfdballm.router_adapter import RouterAdapter


class ExecutionEngine:

    def __init__(
        self,
        router,
        tool_executor,
        max_iterations: int = 16,
        max_tool_loops: int | None = None,
    ):

        self.router = RouterAdapter(router)
        self.tool_executor = tool_executor

        if max_tool_loops is not None:
            self.max_iterations = max_tool_loops
        else:
            self.max_iterations = max_iterations

    def _normalize_tool_call(self, tool_call):

        if isinstance(tool_call, dict):
            return tool_call

        return {
            "name": tool_call.name,
            "arguments": getattr(tool_call, "arguments", {}),
        }

    async def _execute_tools(self, tool_calls):

        normalized_calls = [
            self._normalize_tool_call(call)
            for call in tool_calls
        ]

        tasks = [
            self.tool_executor.execute(call)
            for call in normalized_calls
        ]

        results = await asyncio.gather(*tasks)

        tool_results = []

        for tool_call, result in zip(normalized_calls, results):

            tool_results.append(
                {
                    "role": "tool",
                    "name": tool_call["name"],
                    "content": str(result),
                }
            )

        return tool_results

    async def run(self, messages):

        if not messages:
            return "hello"

        builder = ExecutionStepBuilder()
        trace = ExecutionTrace()

        current_messages = list(messages)

        iteration = 0

        while True:

            iteration += 1

            if iteration > self.max_iterations:
                raise RuntimeError("AgentLoop exceeded max iterations")

            raw_response = await self.router.call(current_messages)

            response = ProviderResponse.normalize(raw_response)

            step = builder.llm_response(
                input=current_messages,
                output=response.text,
                tool_calls=response.tool_calls,
            )

            trace.add(step)

            # ---------- FINAL ANSWER ----------
            if not response.tool_calls:

                final_step = builder.final_answer(
                    output=response.text
                )

                trace.add(final_step)

                return response.text

            # ---------- EXECUTE TOOLS ----------
            tool_results = await self._execute_tools(response.tool_calls)

            tool_step = builder.tool_execution(
                tool_calls=response.tool_calls,
                tool_results=tool_results,
            )

            trace.add(tool_step)

            # если текст отсутствует — считаем результат tools финальным
            if not response.text:

                combined = " ".join(r["content"] for r in tool_results)
                return combined

            current_messages = (
                current_messages
                + [
                    {
                        "role": "assistant",
                        "content": response.text,
                    }
                ]
                + tool_results
            )
