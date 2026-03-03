# mfdballm/providers/gemini.py

import os
import requests
from typing import List, Dict

from mfdballm.providers.base import BaseProvider
from mfdballm.exceptions import (
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)
from mfdballm.config import get_gemini_model


class GeminiProvider(BaseProvider):
    """
    Production-grade Gemini v1 provider.

    - Uses stable v1 endpoint
    - Model configurable via ENV
    - No hardcoded API versions
    - Fully compliant with BaseProvider
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1"

    def __init__(self):
        super().__init__("gemini")

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ProviderUnavailableError("GEMINI_API_KEY not set")

        self.model = get_gemini_model()

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    # ============================================================
    # BaseProvider contract
    # ============================================================

    def health(self) -> bool:
        return bool(self.api_key)

    # ============================================================
    # Chat
    # ============================================================

    def chat(self, messages: List[Dict], timeout: int = 30) -> str:

        contents = []

        for msg in messages:
            role = "user" if msg["role"] != "assistant" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}],
            })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2
            }
        }

        url = (
            f"{self.BASE_URL}/models/"
            f"{self.model}:generateContent"
            f"?key={self.api_key}"
        )

        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=timeout,
            )
        except requests.Timeout:
            raise ProviderTimeoutError("Gemini timeout")
        except requests.RequestException as e:
            raise ProviderUnavailableError(str(e))

        if response.status_code == 429:
            raise ProviderRateLimitError("Gemini rate limited")

        if response.status_code == 404:
            raise ProviderUnavailableError(
                f"Gemini model '{self.model}' not found (404)"
            )

        if not response.ok:
            raise ProviderUnavailableError(
                f"Gemini error {response.status_code}: {response.text}"
            )

        try:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            raise ProviderUnavailableError(
                "Gemini invalid response format"
            )
