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

        self.max_tool_loops = (
            max_tool_loops if max_tool_loops is not None else max_iterations
        )

    # ---------------------------------------------------------
    # TOOL NORMALIZATION
    # ---------------------------------------------------------

    def _normalize_tool_call(self, tool_call):

        if isinstance(tool_call, dict):

            if "function" in tool_call:
                fn = tool_call["function"]
                return {
                    "id": tool_call.get("id"),
                    "name": fn.get("name"),
                    "arguments": fn.get("arguments", {}) or {},
                }

            return {
                "id": tool_call.get("id"),
                "name": tool_call.get("name"),
                "arguments": tool_call.get("arguments", {}) or {},
            }

        name = getattr(tool_call, "name", None)
        arguments = getattr(tool_call, "arguments", {}) or {}

        if hasattr(tool_call, "function"):
            fn = getattr(tool_call, "function")
            name = getattr(fn, "name", name)
            arguments = getattr(fn, "arguments", arguments)

        return {
            "id": getattr(tool_call, "id", None),
            "name": name,
            "arguments": arguments or {},
        }

    # ---------------------------------------------------------
    # TOOL EXECUTION
    # ---------------------------------------------------------

    async def _execute_tools(self, tool_calls):

        normalized = [
            self._normalize_tool_call(call)
            for call in tool_calls
        ]

        tasks = []

        for call in normalized:

            name = call["name"]
            args = call["arguments"]

            try:
                task = self.tool_executor.execute(name, args)
            except TypeError:
                task = self.tool_executor.execute(call)

            tasks.append(task)

        results = await asyncio.gather(*tasks)

        tool_results = []

        for call, result in zip(normalized, results):

            tool_results.append(
                {
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "name": call["name"],
                    "content": "" if result is None else str(result),
                }
            )

        return tool_results

    # ---------------------------------------------------------
    # TEXT EXTRACTION
    # ---------------------------------------------------------

    def _extract_text(self, raw):

        if raw is None:
            return ""

        if isinstance(raw, str):
            return raw

        if isinstance(raw, dict):

            if "output" in raw:
                return raw["output"] or ""

            if "text" in raw:
                return raw["text"] or ""

            if "content" in raw:

                content = raw["content"]

                if isinstance(content, str):
                    return content

                if isinstance(content, list):

                    parts = []

                    for item in content:
                        if isinstance(item, dict):

                            if "text" in item:
                                parts.append(item["text"])

                            elif "content" in item:
                                parts.append(item["content"])

                    return "".join(parts)

            if "message" in raw:
                msg = raw["message"]
                if isinstance(msg, dict):
                    return msg.get("content", "")

            if "choices" in raw:
                choices = raw["choices"]

                if choices:
                    msg = choices[0].get("message", {})
                    return msg.get("content", "")

        if hasattr(raw, "text"):
            value = getattr(raw, "text")
            if value:
                return value

        if hasattr(raw, "content"):

            content = getattr(raw, "content")

            if isinstance(content, str):
                return content

            if isinstance(content, list):

                parts = []

                for item in content:
                    if hasattr(item, "text"):
                        parts.append(item.text)

                return "".join(parts)

        return ""

    # ---------------------------------------------------------
    # TOOL CALL EXTRACTION
    # ---------------------------------------------------------

    def _extract_tool_calls(self, raw):

        if isinstance(raw, dict):

            if "tool_calls" in raw:
                return raw["tool_calls"]

            if "choices" in raw:
                choices = raw["choices"]

                if choices:
                    msg = choices[0].get("message", {})
                    return msg.get("tool_calls", [])

        if hasattr(raw, "tool_calls"):
            return getattr(raw, "tool_calls")

        return []

    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------

    async def run(self, messages):

        if not messages:
            return "hello"

        builder = ExecutionStepBuilder()
        trace = ExecutionTrace()

        current_messages = list(messages)

        tool_loops = 0
        last_text = ""

        while True:

            raw_response = await self.router.call(current_messages)

            response = ProviderResponse.normalize(raw_response)

            tool_calls = response.tool_calls or self._extract_tool_calls(raw_response)

            text = response.text

            if not text:
                text = self._extract_text(raw_response)

            if text:
                last_text = text

            step = builder.llm_response(
                input=current_messages,
                output=text,
                tool_calls=tool_calls,
            )

            trace.add(step)

            if text and not tool_calls:
                final_step = builder.final_answer(output=text)
                trace.add(final_step)
                return text

            if tool_loops >= self.max_tool_loops:
                return last_text or ""

            if not tool_calls:
                return last_text or ""

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
