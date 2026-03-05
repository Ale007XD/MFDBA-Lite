import asyncio

from mfdballm.provider_registry import build_providers
from mfdballm.router import Router
from mfdballm.agent.agent_loop import AgentLoop

from mfdballm.tools.base_tool import BaseTool


class HelloTool(BaseTool):
    name = "hello_tool"
    description = "Returns hello message"

    parameters = {
        "type": "object",
        "properties": {},
    }

    async def run(self, **kwargs):
        return "Hello from tool!"


async def main():

    providers = build_providers()

    router = Router(providers)

    tools = [HelloTool()]

    agent = AgentLoop(
        router=router,
        tools=tools,
    )

    result = await agent.run(
        "Use hello_tool and show the result."
    )

    print("\nFINAL RESULT:", result)


if __name__ == "__main__":
    asyncio.run(main())
