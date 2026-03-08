import asyncio
from typing import List, Dict, Any, Optional

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

        self.max_tool_loops = (
            max_tool_loops if max_tool_loops is not None else max_iterations
        )

    # ---------------------------------------------------------
    # TOOL EXECUTION
    # ---------------------------------------------------------

    async def _execute_tools(self, tool_calls):

        tasks = []

        for call in tool_calls:

            name = call.name
            args = call.arguments or {}

            try:
                task = self.tool_executor.execute(name, args)
            except TypeError:
                task = self.tool_executor.execute(call)

            tasks.append(task)

        results = await asyncio.gather(*tasks)

        tool_results = []

        for call, result in zip(tool_calls, results):

            tool_results.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": call.name,
                    "content": "" if result is None else str(result),
                }
            )

        return tool_results

    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------

    async def run(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[list] = None,
    ) -> str:

        if not messages:
            return "hello"

        builder = ExecutionStepBuilder()
        trace = ExecutionTrace()

        current_messages = list(messages)

        tool_loops = 0
        last_text = ""

        while True:

            # -------------------------------------------------
            # LLM CALL
            # -------------------------------------------------

            response: ProviderResponse = await self.router.call(
                current_messages,
                tools=tools,
            )

            text = response.text or ""
            tool_calls = response.tool_calls

            if text:
                last_text = text

            step = builder.llm_response(
                input=current_messages,
                output=text,
                tool_calls=tool_calls,
            )

            trace.add(step)

            # -------------------------------------------------
            # FINAL ANSWER
            # -------------------------------------------------

            if text and not tool_calls:
                final_step = builder.final_answer(output=text)
                trace.add(final_step)
                return text

            # -------------------------------------------------
            # LOOP LIMIT
            # -------------------------------------------------

            if tool_loops >= self.max_tool_loops:
                return last_text or ""

            if not tool_calls:
                return last_text or ""

            # -------------------------------------------------
            # TOOL EXECUTION
            # -------------------------------------------------

            tool_loops += 1

            tool_results = await self._execute_tools(tool_calls)

            tool_step = builder.tool_execution(
                tool_calls=tool_calls,
                tool_results=tool_results,
            )

            trace.add(tool_step)

            new_messages = []

            if text:
                new_messages.append(
                    {
                        "role": "assistant",
                        "content": text,
                    }
                )

            current_messages = (
                current_messages
                + new_messages
                + tool_results
            )
