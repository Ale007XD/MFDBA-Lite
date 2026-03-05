import asyncio

from mfdballm.provider_registry import ProviderRegistry
from mfdballm.router import Router
from mfdballm.agent.agent_loop import AgentLoop


async def main():

    registry = ProviderRegistry()
    registry.load_from_env()

    router = Router(registry.get_providers())

    agent = AgentLoop(router)

    result = await agent.run("Say hello in one short sentence")

    print("RESULT:", result)


if __name__ == "__main__":
    asyncio.run(main())
