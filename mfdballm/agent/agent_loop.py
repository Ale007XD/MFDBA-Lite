import json

from mfdballm.tools.tool_prompt import build_tools_prompt
from mfdballm.tools.tool_executor import execute_tool


class AgentLoop:

    def __init__(self, router, tools=None, max_iterations=5):

        self.router = router
        self.tools = tools or []
        self.max_iterations = max_iterations

    async def run(self, messages):

        # Inject tool schema into system prompt
        system_prompt = build_tools_prompt(self.tools)

        messages = [
            {"role": "system", "content": system_prompt}
        ] + messages

        for _ in range(self.max_iterations):

            response = await self.router.chat(messages)

            messages.append({
                "role": "assistant",
                "content": response
            })

            # detect tool call
            try:
                data = json.loads(response)
            except Exception:
                return response

            if "tool" not in data:
                return response

            tool_name = data["tool"]
            args = data.get("args", {})

            result = execute_tool(tool_name, args, self.tools)

            messages.append({
                "role": "tool",
                "content": json.dumps(result)
            })

        return "Max agent iterations reached"
