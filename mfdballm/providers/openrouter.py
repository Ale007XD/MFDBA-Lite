# mfdballm/providers/openrouter.py

import os
import requests
import time
from typing import List, Dict

from mfdballm.providers.base import BaseProvider
from mfdballm.exceptions import (
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)


FREE_MODELS = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemma-2-9b-it:free",
    "mistralai/mistral-7b-instruct:free",
]


class OpenRouterProvider(BaseProvider):

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self):
        super().__init__("openrouter")

        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ProviderUnavailableError("OPENROUTER_API_KEY not set")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def _call_model(self, model: str, messages, timeout):
        payload = {
            "model": model,
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
            raise ProviderTimeoutError("OpenRouter timeout")
        except requests.RequestException as e:
            raise ProviderUnavailableError(str(e))

        if response.status_code == 429:
            raise ProviderRateLimitError("OpenRouter rate limited")

        if response.status_code == 404:
            return None

        if not response.ok:
            raise ProviderUnavailableError(
                f"OpenRouter error {response.status_code}: {response.text}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def chat(self, messages: List[Dict], timeout=30) -> str:
        for model in FREE_MODELS:
            result = self._call_model(model, messages, timeout)
            if result:
                return result
            time.sleep(1)

        raise ProviderUnavailableError("All FREE OpenRouter models failed")

    def health(self) -> bool:
        return bool(self.api_key)
