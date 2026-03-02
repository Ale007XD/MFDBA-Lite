import os
import requests

from .base import BaseProvider


class OpenRouterProvider(BaseProvider):

    def __init__(self):
        super().__init__("openrouter")
        self.api_key = os.getenv("OPENROUTER_API_KEY")

    def chat(self, messages, timeout=None):
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json={"messages": messages},
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=timeout,
        )

        response.raise_for_status()
        return response.json()

    def health(self) -> bool:
        return True
