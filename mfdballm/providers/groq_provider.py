import httpx
from typing import List, Dict

from mfdballm.providers.base_provider import BaseProvider
from mfdballm.types import ProviderResponse


class GroqProvider(BaseProvider):
    """
    Groq LLM Provider
    """

    def __init__(self, api_key: str, model: str = "llama3-70b-8192"):
        super().__init__(name="groq", api_key=api_key, model=model)
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    async def chat(self, messages: list[dict], tools=None) -> ProviderResponse:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.url, headers=headers, json=payload)

        response.raise_for_status()

        data = response.json()

        text = data["choices"][0]["message"]["content"]

        return ProviderResponse(
            text=text,
            raw=data
        )
