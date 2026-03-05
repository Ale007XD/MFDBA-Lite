import asyncio

from mfdballm.provider_registry import build_providers
from mfdballm.router import Router


async def main():

    providers = build_providers()

    router = Router(providers)

    messages = [
        {"role": "user", "content": "Say hello in one sentence."}
    ]

    response = await router.chat(messages)

    print("\nMODEL RESPONSE:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
