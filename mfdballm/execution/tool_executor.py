import time
import inspect

from mfdballm.models.tool_result import ToolResult


class ToolExecutor:

    def __init__(self, registry):
        self.registry = registry

    async def execute(self, tool_or_name, args: dict | None = None):

        # --- ToolCall object ---
        if hasattr(tool_or_name, "name"):

            tool_name = tool_or_name.name
            arguments = tool_or_name.arguments or {}

        # --- dict tool call (LLM / tests / routers) ---
        elif isinstance(tool_or_name, dict):

            tool_name = tool_or_name.get("name")
            arguments = tool_or_name.get("arguments", {}) or {}

        # --- plain tool name ---
        else:

            tool_name = tool_or_name
            arguments = args or {}

        tool_name = str(tool_name).lower()

        tool = self.registry.get(tool_name)

        if tool is None:
            return ToolResult(
                tool_name=tool_name,
                output=None,
                success=False,
                execution_time_ms=0,
                error=f"Tool not found: {tool_name}"
            )

        start = time.time()

        try:

            run_fn = tool.run

            # --- attempt 1: run(**kwargs) ---
            try:

                if inspect.iscoroutinefunction(run_fn):
                    result = await run_fn(**arguments)
                else:
                    result = run_fn(**arguments)

            except TypeError:

                # --- attempt 2: run(arguments) ---
                if inspect.iscoroutinefunction(run_fn):
                    result = await run_fn(arguments)
                else:
                    result = run_fn(arguments)

            elapsed = int((time.time() - start) * 1000)

            return ToolResult(
                tool_name=tool_name,
                output=result,
                success=True,
                execution_time_ms=elapsed
            )

        except Exception as e:

            elapsed = int((time.time() - start) * 1000)

            return ToolResult(
                tool_name=tool_name,
                output=None,
                success=False,
                execution_time_ms=elapsed,
                error=str(e)
            )
