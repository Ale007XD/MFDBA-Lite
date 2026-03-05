from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseProvider(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    async def chat(self, messages: List[Dict[str, Any]]) -> str:
        """
        Execute chat completion.

        messages format:
        [
            {"role": "user", "content": "..."}
        ]
        """
        pass
