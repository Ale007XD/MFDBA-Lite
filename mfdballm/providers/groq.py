from .base import BaseProvider


class GroqProvider(BaseProvider):

    def __init__(self):
        super().__init__("groq")

    def chat(self, messages, timeout=None):
        return {"response": "groq"}

    def health(self) -> bool:
        return True
