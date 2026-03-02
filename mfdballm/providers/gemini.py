from .base import BaseProvider


class GeminiProvider(BaseProvider):

    def __init__(self):
        super().__init__("gemini")

    def chat(self, messages, timeout=None):
        return {"response": "gemini"}

    def health(self) -> bool:
        return True
