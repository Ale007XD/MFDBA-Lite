import httpx


class GeminiProvider:

    def __init__(self, config):

        self.name = "gemini"
        self.model = config["model"]
        self.api_key = config["api_key"]

    async def chat(self, messages, tools=None):

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )

        contents = []

        for m in messages:

            role = "user"

            if m["role"] == "assistant":
                role = "model"

            contents.append({
                "role": role,
                "parts": [{"text": m["content"]}]
            })

        payload = {
            "contents": contents
        }

        async with httpx.AsyncClient(timeout=60) as client:

            r = await client.post(
                url,
                json=payload
            )

        r.raise_for_status()

        data = r.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]
