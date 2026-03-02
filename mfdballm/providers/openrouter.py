# mfdballm/providers/openrouter.py

import os
import requests
import time
from typing import List, Dict, Any


FREE_MODELS = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemma-2-9b-it:free",
    "mistralai/mistral-7b-instruct:free",
]


class OpenRouterProvider:

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY not set")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://mfdbalite.local",
            "X-Title": "MFDBA-Lite",
        })

    def _try_model(self, model: str, messages, timeout, temperature):
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }

        response = self.session.post(
            self.BASE_URL,
            json=payload,
            timeout=timeout,
        )

        if response.status_code in (404, 429):
            return None

        if not response.ok:
            raise RuntimeError(
                f"OpenRouter error {response.status_code}:\n{response.text}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def chat(
        self,
        messages: List[Dict[str, str]],
        timeout: int = 30,
        temperature: float = 0.7,
    ) -> str:

        for model in FREE_MODELS:
            try:
                result = self._try_model(model, messages, timeout, temperature)
                if result:
                    return result
            except Exception:
                continue

            time.sleep(1)

        raise RuntimeError("All FREE OpenRouter models unavailable")
