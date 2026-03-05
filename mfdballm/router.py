from typing import List, Dict, Any

from mfdballm.providers.base_provider import BaseProvider
from mfdballm.providers.response import ProviderResponse


class Router:
    """
    Router selects providers and performs failover.

    Strategy:
    - iterate providers in order
    - try generate()
    - on failure → fallback to next provider
    """

    def __init__(self, providers: List[BaseProvider]):
        if not providers:
            raise RuntimeError("Router requires at least one provider")

        self.providers = providers

    async def generate(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] | None = None,
    ) -> ProviderResponse:

        last_error = None

        for provider in self.providers:

            try:
                response = await provider.generate(
                    messages=messages,
                    tools=tools
                )

                return response

            except Exception as e:

                print(f"[Router] provider failed: {provider.name} -> {e}")

                last_error = e

        raise RuntimeError(f"All providers failed: {last_error}")
