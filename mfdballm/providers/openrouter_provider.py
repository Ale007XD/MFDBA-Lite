import httpx


class OpenRouterProvider:

    def __init__(self, config):

        self.name = "openrouter"
        self.model = config["model"]
        self.api_key = config["api_key"]

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def chat(self, messages, tools=None):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages
        }

        async with httpx.AsyncClient(timeout=60) as client:

            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]
