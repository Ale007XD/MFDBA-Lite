import json

from .tool_parser import parse_tool_call


class Agent:

    def __init__(self, router, tool_executor, max_steps=8):
        self.router = router
        self.tool_executor = tool_executor
        self.max_steps = max_steps

    async def run(self, messages):

        for _ in range(self.max_steps):

            response = await self.router.chat(messages)

            tool_call = parse_tool_call(response.text)

            if not tool_call:
                return response.text

            result = await self.tool_executor.execute(
                tool_call["name"],
                tool_call.get("args", {})
            )

            messages.append({
                "role": "tool",
                "content": json.dumps(result)
            })

        return "Agent stopped: step limit"
