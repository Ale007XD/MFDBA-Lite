import os
import httpx

from mfdballm.providers.base import BaseProvider
from mfdballm.types import ProviderResponse
from mfdballm.exceptions import ProviderUnavailableError


OPENROUTER_MODELS = [
    "openrouter/auto",
    "meta-llama/llama-3.1-8b-instruct"
]


class OpenAICompatProvider(BaseProvider):

    name = "openrouter"

    def __init__(self):

        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise Exception("OPENROUTER_API_KEY not set")

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def chat(self, messages):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        last_error = None

        async with httpx.AsyncClient(timeout=60) as client:

            for model in OPENROUTER_MODELS:

                payload = {
                    "model": model,
                    "messages": messages
                }

                try:

                    r = await client.post(
                        self.base_url,
                        headers=headers,
                        json=payload
                    )

                    if r.status_code != 200:
                        last_error = r.text
                        continue

                    data = r.json()

                    text = data["choices"][0]["message"]["content"]

                    return ProviderResponse(
                        text=text,
                        provider=self.name,
                        model=model
                    )

                except Exception as e:
                    last_error = str(e)

        raise ProviderUnavailableError(f"OpenRouter failed: {last_error}")

    def health(self):

        return {
            "provider": self.name,
            "status": "ok"
        }
