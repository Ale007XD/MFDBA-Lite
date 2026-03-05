import os
import requests

from mfdballm.config import get_openrouter_models
from mfdballm.exceptions import ProviderUnavailableError
from mfdballm.providers.base import BaseProvider


class OpenRouterProvider(BaseProvider):

    name = "openrouter"

    def __init__(self):

        self.api_key = os.environ.get("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ProviderUnavailableError("OPENROUTER_API_KEY not set")

        self.models = get_openrouter_models()

    def chat(self, messages):

        last_error = None

        for model in self.models:

            try:

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": messages,
                    },
                    timeout=60,
                )

                data = response.json()

                return data["choices"][0]["message"]["content"]

            except Exception as e:

                last_error = e
                continue

        raise ProviderUnavailableError(
            f"All OpenRouter models failed. Last error: {last_error}"
        )
