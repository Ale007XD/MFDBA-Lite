from abc import ABC, abstractmethod
from typing import Union

from mfdballm.types_tool import ToolCall


class BaseAgent(ABC):

    @abstractmethod
    async def run(self, message: str) -> Union[str, ToolCall]:
        """
        Perform reasoning step.

        Returns either:
        - final text response
        - ToolCall request
        """
        pass
