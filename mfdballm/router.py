from mfdballm.types import ProviderResponse


class Router:
    """
    Fallback router.
    Tries providers sequentially until one succeeds.
    """

    def __init__(self, providers):
        self.providers = providers

    async def chat(self, messages, tools=None) -> ProviderResponse:

        last_error = None

        for provider in self.providers:
            try:
                return await provider.chat(messages, tools=tools)

            except Exception as e:
                last_error = e
                continue

        raise RuntimeError(f"All providers failed: {last_error}")
