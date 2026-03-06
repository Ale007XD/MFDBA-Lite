import asyncio
import os

from mfdballm.providers.openrouter_provider import OpenRouterProvider


async def main():

    if not os.getenv("OPENROUTER_API_KEY"):
        print("OPENROUTER_API_KEY not set")
        return

    provider = OpenRouterProvider()

    response = await provider.generate([
        {"role": "user", "content": "Say hello in one sentence"}
    ])

    print("MODEL:", response.model)
    print("CONTENT:", response.content)


if __name__ == "__main__":
    asyncio.run(main())
