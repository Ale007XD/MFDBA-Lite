from abc import ABC, abstractmethod
from typing import List, Dict, Any

from mfdballm.providers.response import ProviderResponse


class BaseProvider(ABC):

    name: str = "base"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key
        self.model = model

    def is_configured(self) -> bool:
        return self.api_key is not None

    async def generate(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] | None = None,
    ) -> ProviderResponse:

        return await self.chat(messages, tools)

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] | None = None,
    ) -> ProviderResponse:
        pass
