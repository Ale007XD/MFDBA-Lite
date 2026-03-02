# mfdballm/providers/cluster.py

from .openrouter import OpenRouterProvider
from .groq import GroqProvider


class FreeClusterProvider:

    def __init__(self):
        self.providers = []

        try:
            self.providers.append(OpenRouterProvider())
        except Exception:
            pass

        try:
            self.providers.append(GroqProvider())
        except Exception:
            pass

        if not self.providers:
            raise RuntimeError("No providers available")

    def chat(self, messages, timeout=30):

        for provider in self.providers:
            try:
                return provider.chat(messages, timeout=timeout)
            except Exception:
                continue

        raise RuntimeError("All providers failed")
