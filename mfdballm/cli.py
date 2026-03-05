import argparse
import asyncio

from mfdballm.router import Router
from mfdballm.provider_registry import build_providers
from mfdballm.agent.agent_loop import AgentLoop

# tools
from mfdballm.tools.echo import EchoTool


async def async_main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        choices=["chat"]
    )

    parser.add_argument(
        "message",
        nargs="?"
    )

    args = parser.parse_args()

    providers = build_providers()

    router = Router(providers)

    tools = [
        EchoTool()
    ]

    agent = AgentLoop(
        router=router,
        tools=tools
    )

    if args.command == "chat":

        messages = [
            {
                "role": "user",
                "content": args.message
            }
        ]

        result = await agent.run(messages)

        print(result)


def main():
    asyncio.run(async_main())
