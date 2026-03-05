from typing import List, Dict, Any, Callable

from mfdballm.router import Router
from mfdballm.providers.response import ProviderResponse
from mfdballm.tools.tool_executor import ToolExecutor
from mfdballm.tools.schemas import build_schemas
from mfdballm.tools.tool_parser import ToolCallParser


class AgentLoop:

    def __init__(self, router: Router, tools: Dict[str, Callable] | None = None):

        self.router = router
        self.tools = tools or {}

        self.executor = ToolExecutor(self.tools)

        self.tool_schemas = build_schemas(self.tools)

    async def run(self, user_message: str) -> str:

        messages: List[Dict[str, Any]] = [
            {
                "role": "user",
                "content": user_message
            }
        ]

        while True:

            response: ProviderResponse = await self.router.generate(
                messages=messages,
                tools=self.tool_schemas if self.tools else None
            )

            # 1 structured tool call
            tool_call = response.tool_call

            # 2 textual tool call fallback
            if tool_call is None:
                tool_call = ToolCallParser.parse(response.content or "")

            # 3 normal response
            if tool_call is None:
                return response.content or ""

            tool_name = tool_call["name"]
            arguments = tool_call["arguments"]

            result = self.executor.execute(tool_name, arguments)

            messages.append({
                "role": "assistant",
                "content": None,
                "tool_call": tool_call
            })

            messages.append({
                "role": "tool",
                "content": str(result)
            })
