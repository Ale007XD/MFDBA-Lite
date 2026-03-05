import asyncio

from mfdballm.provider_registry import ProviderRegistry
from mfdballm.router import Router
from mfdballm.agent.agent_loop import AgentLoop


def hello_tool():

    return "Hello from tool!"


async def main():

    registry = ProviderRegistry()
    registry.load_from_env()

    router = Router(registry.get_providers())

    tools = {
        "hello_tool": hello_tool
    }

    agent = AgentLoop(router, tools)

    result = await agent.run(
        "Use the hello_tool and tell me the result"
    )

    print("FINAL RESULT:", result)


if __name__ == "__main__":
    asyncio.run(main())
