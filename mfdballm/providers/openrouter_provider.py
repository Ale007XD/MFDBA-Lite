from typing import Any, Dict

from mfdballm.providers.base_provider import BaseProvider
from mfdballm.types_provider_metadata import ProviderMetadata


class OpenRouterProvider(BaseProvider):
    """
    Provider для OpenRouter API.
    """

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @property
    def metadata(self) -> ProviderMetadata:
        """
        Метаданные провайдера.
        """
        return ProviderMetadata(
            name="openrouter",
            models=[self.model],
            supports_tools=True,
            supports_stream=True,
            max_context_tokens=128000,
        )

    async def generate(self, prompt: str, **kwargs: Dict[str, Any]) -> str:
        """
        Генерация ответа.
        (пока stub для тестов)
        """
        return f"[OpenRouter mock response for: {prompt}]"
