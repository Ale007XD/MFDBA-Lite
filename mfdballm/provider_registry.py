import os
from typing import List

from mfdballm.providers.base_provider import BaseProvider
from mfdballm.providers.openrouter_provider import OpenRouterProvider


class ProviderRegistry:
    """
    Central registry that instantiates and manages providers.

    Responsibilities:
    - detect configured providers
    - instantiate them
    - provide ordered provider list for Router
    """

    def __init__(self):
        self.providers: List[BaseProvider] = []

    def load_from_env(self):
        """
        Load providers based on available environment variables.
        """

        providers: List[BaseProvider] = []

        # OpenRouter
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            providers.append(
                OpenRouterProvider(api_key=openrouter_key)
            )

        self.providers = providers

    def get_providers(self) -> List[BaseProvider]:
        """
        Return active providers.
        """

        return self.providers
