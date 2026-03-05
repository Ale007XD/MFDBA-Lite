import httpx
from typing import List, Dict

from mfdballm.base_provider import BaseProvider


class GeminiProvider(BaseProvider):
    """
    Google Gemini Provider
    """

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        super().__init__(name="gemini", api_key=api_key, model=model)

        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    async def generate(self, messages: List[Dict]) -> str:

        prompt = "\n".join([m["content"] for m in messages])

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        params = {
            "key": self.api_key
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self.url,
                params=params,
                json=payload,
            )

        response.raise_for_status()

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]
