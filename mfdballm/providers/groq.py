# mfdballm/providers/groq.py

import os
import requests
from typing import List, Dict

from mfdballm.providers.base import BaseProvider
from mfdballm.exceptions import (
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)


class GroqProvider(BaseProvider):

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama-3.1-8b-instant"

    def __init__(self):
        super().__init__("groq")

        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ProviderUnavailableError("GROQ_API_KEY not set")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def chat(self, messages: List[Dict], timeout=30) -> str:
        payload = {
            "model": self.MODEL,
            "messages": messages,
            "temperature": 0.2,
        }

        try:
            response = self.session.post(
                self.BASE_URL,
                json=payload,
                timeout=timeout,
            )
        except requests.Timeout:
            raise ProviderTimeoutError("Groq timeout")
        except requests.RequestException as e:
            raise ProviderUnavailableError(str(e))

        if response.status_code == 429:
            raise ProviderRateLimitError("Groq rate limited")

        if not response.ok:
            raise ProviderUnavailableError(
                f"Groq error {response.status_code}: {response.text}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def health(self) -> bool:
        return bool(self.api_key)
