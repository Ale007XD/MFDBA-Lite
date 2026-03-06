from abc import ABC, abstractmethod

from mfdballm.types_provider_metadata import ProviderMetadata
from mfdballm.types import ProviderResponse


class BaseProvider(ABC):

    @property
    @abstractmethod
    def metadata(self) -> ProviderMetadata:
        """
        Static provider capability description.
        """
        pass

    @abstractmethod
    async def generate(self, prompt: str) -> ProviderResponse:
        """
        Execute model request.
        """
        pass
