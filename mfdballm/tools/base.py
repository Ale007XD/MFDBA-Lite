from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):

    name: str
    description: str

    @abstractmethod
    async def run(self, args: Dict[str, Any]) -> Any:
        pass
