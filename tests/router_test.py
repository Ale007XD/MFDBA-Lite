import asyncio
import json

from mfdballm.router import Router
from mfdballm.provider_registry import build_providers


async def main():

    with open("config/config.default.json") as f:
        config = json.load(f)

    providers = build_providers(config)

    router = Router(providers)

    messages = [
        {"role": "user", "content": "Hello!"}
    ]

    response = await router.chat(messages)

    print("MODEL RESPONSE:")
    print(response)


asyncio.run(main())
