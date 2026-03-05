import argparse
import asyncio

from mfdballm.provider_registry import ProviderRegistry
from mfdballm.router import Router


async def run_chat(user_message: str):

    # Load providers
    registry = ProviderRegistry()
    registry.load_from_env()

    providers = registry.get_providers()

    if not providers:
        raise RuntimeError("No providers configured")

    # Create router
    router = Router(providers)

    # Build message list
    messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    # Call LLM
    response = await router.generate(messages)

    # Output result
    print(response.content)


def main():

    parser = argparse.ArgumentParser(
        prog="mfdballm",
        description="MFDBA-Lite Local AI Execution Engine"
    )

    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser("chat")
    chat_parser.add_argument("message", type=str)

    args = parser.parse_args()

    if args.command == "chat":

        asyncio.run(
            run_chat(args.message)
        )

    else:

        parser.print_help()


if __name__ == "__main__":
    main()
