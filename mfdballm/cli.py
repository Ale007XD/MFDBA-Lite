import argparse
import asyncio
import json

from mfdballm.provider_registry import build_providers
from mfdballm.router import Router


async def run_chat(user_message: str):

    # Load config
    with open("config/config.default.json") as f:
        config = json.load(f)

    # Build providers
    providers = build_providers(config)

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
