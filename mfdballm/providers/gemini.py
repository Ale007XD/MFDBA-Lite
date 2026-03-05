import os
import json
import aiohttp

from mfdballm.exceptions import ProviderUnavailableError


class GeminiProvider:
    name = "gemini"

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        # стабильная модель
        self.model = "gemini-2.0-flash"

        self.endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )

    async def chat(self, messages):

        contents = []

        for m in messages:
            role = "user"
            if m["role"] == "assistant":
                role = "model"

            contents.append(
                {
                    "role": role,
                    "parts": [{"text": m["content"]}]
                }
            )

        payload = {
            "contents": contents
        }

        last_error = None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.endpoint, json=payload) as resp:

                    text = await resp.text()

                    if resp.status != 200:
                        last_error = text
                        raise Exception(text)

                    data = json.loads(text)

                    candidates = data.get("candidates", [])
                    if not candidates:
                        raise Exception("No candidates returned")

                    parts = candidates[0]["content"]["parts"]

                    output = ""
                    for p in parts:
                        if "text" in p:
                            output += p["text"]

                    return output.strip()

        except Exception as e:
            last_error = str(e)

        raise ProviderUnavailableError(f"Gemini failed: {last_error}")
