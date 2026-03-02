# mfdballm/providers/groq.py

import os
import requests
from typing import List, Dict


class GroqProvider:

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY not set")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def chat(self, messages: List[Dict[str, str]], timeout=30):

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.7,
        }

        response = self.session.post(
            self.BASE_URL,
            json=payload,
            timeout=timeout,
        )

        if not response.ok:
            raise RuntimeError(
                f"Groq error {response.status_code}:\n{response.text}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]
