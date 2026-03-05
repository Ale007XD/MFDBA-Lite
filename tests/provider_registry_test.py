import os

from mfdballm.provider_registry import ProviderRegistry


def main():

    if not os.getenv("OPENROUTER_API_KEY"):
        print("OPENROUTER_API_KEY not set")
        return

    registry = ProviderRegistry()

    registry.load_from_env()

    providers = registry.get_providers()

    print("PROVIDERS LOADED:", len(providers))

    for p in providers:
        print(" -", p.name)


if __name__ == "__main__":
    main()
