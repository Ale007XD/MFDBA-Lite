import asyncio

from mfdballm.provider_registry import ProviderRegistry
from mfdballm.router import Router


async def main():

    registry = ProviderRegistry()
    registry.load_from_env()

    providers = registry.get_providers()

    router = Router(providers)

    response = await router.generate([
        {
            "role": "user",
            "content": "Say hello in one short sentence"
        }
    ])

    print("MODEL:", response.model)
    print("CONTENT:", response.content)


if __name__ == "__main__":
    asyncio.run(main())
