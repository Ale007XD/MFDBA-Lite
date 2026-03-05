import httpx

from mfdballm.providers.base_provider import BaseProvider
from mfdballm.types import ProviderResponse


class GeminiProvider(BaseProvider):

    def __init__(self, api_key: str, model: str):
        super().__init__(name="gemini", api_key=api_key, model=model)

    async def chat(self, messages, tools=None):

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )

        contents = []

        for m in messages:

            role = "user"

            if m["role"] == "assistant":
                role = "model"

            contents.append({
                "role": role,
                "parts": [{"text": m["content"]}]
            })

        payload = {
            "contents": contents
        }

        async with httpx.AsyncClient(timeout=60) as client:

            r = await client.post(
                url,
                json=payload
            )

        r.raise_for_status()

        data = r.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]

        return ProviderResponse(
            text=text,
            raw=data
        )
