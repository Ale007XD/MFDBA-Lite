from abc import ABC, abstractmethod


class BaseProvider(ABC):

    def __init__(self, name: str, api_key: str, model: str, base_url: str | None = None):
        self.name = name
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    @abstractmethod
    async def chat(self, messages: list[dict], tools: list | None = None) -> str:
        """
        Universal chat interface for all providers.
        """
        pass

    async def health(self) -> bool:
        return True
