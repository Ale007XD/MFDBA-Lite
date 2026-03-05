import os
import httpx
from typing import List, Dict, Any

from mfdballm.providers.base_provider import BaseProvider
from mfdballm.providers.response import ProviderResponse


class OpenRouterProvider(BaseProvider):

    name = "openrouter"

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "openrouter/free"
    ):
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")

        super().__init__(api_key=api_key, model=model)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] | None = None,
    ) -> ProviderResponse:

        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            payload["tools"] = tools

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self.API_URL,
                headers=headers,
                json=payload
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"OpenRouter error {response.status_code}: {response.text}"
            )

        data = response.json()

        message = data["choices"][0]["message"]

        content = message.get("content")

        tool_call = None

        if "tool_calls" in message:
            tool = message["tool_calls"][0]

            tool_call = {
                "name": tool["function"]["name"],
                "arguments": tool["function"]["arguments"]
            }

        return ProviderResponse(
            content=content,
            model=data.get("model", self.model),
            tool_call=tool_call
        )
