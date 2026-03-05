import httpx

from mfdballm.providers.base_provider import BaseProvider
from mfdballm.types import ProviderResponse


class OpenRouterProvider(BaseProvider):

    def __init__(self, api_key: str, model: str):
        super().__init__(
            name="openrouter",
            api_key=api_key,
            model=model,
            base_url="https://openrouter.ai/api/v1/chat/completions"
        )

    async def chat(self, messages, tools=None):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages
        }

        async with httpx.AsyncClient(timeout=60) as client:

            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload
            )

        response.raise_for_status()

        data = response.json()

        text = data["choices"][0]["message"]["content"]

        return ProviderResponse(
            text=text,
            raw=data
        )
