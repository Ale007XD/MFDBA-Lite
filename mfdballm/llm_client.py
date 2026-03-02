# mfdballm/llm_client.py

from typing import List, Dict

from mfdballm.provider_registry import build_providers
from mfdballm.router import Router


class LLMClient:
    """
    Thin facade over Router.
    No fallback logic.
    No rate limiting.
    No model selection.
    """

    def __init__(self):
        providers = build_providers()
        self.router = Router(providers)

    def chat(self, messages: List[Dict]) -> str:
        return self.router.chat(messages)
