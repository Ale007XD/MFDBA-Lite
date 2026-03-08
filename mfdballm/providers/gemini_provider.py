from typing import Any, Dict

from mfdballm.providers.base_provider import BaseProvider
from mfdballm.types_provider_metadata import ProviderMetadata


class GeminiProvider(BaseProvider):
    """
    Provider для Google Gemini API.
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
            name="gemini",
            models=[self.model],
            supports_tools=False,
            supports_stream=False,
            max_context_tokens=32768,
        )

    async def generate(self, prompt: str, **kwargs: Dict[str, Any]) -> str:
        """
        Генерация ответа.
        (пока stub для тестов)
        """
        return f"[Gemini mock response for: {prompt}]"
