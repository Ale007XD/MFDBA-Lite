from typing import Any, Dict, List

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

    async def chat(self, messages: List[Dict[str, Any]], **kwargs: Dict[str, Any]) -> str:
        """
        Унифицированный интерфейс чата для Router.

        messages:
            [
                {"role": "system", "content": "..."},
                {"role": "user", "content": "..."}
            ]
        """

        # Простейшее преобразование messages → prompt
        prompt_parts = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt_parts.append(f"{role}: {content}")

        prompt = "\n".join(prompt_parts)

        return await self.generate(prompt, **kwargs)

    async def generate(self, prompt: str, **kwargs: Dict[str, Any]) -> str:
        """
        Генерация ответа.
        (stub для тестов)
        """
        return f"[OpenRouter mock response for: {prompt}]"
