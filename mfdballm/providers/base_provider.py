from mfdballm.types_provider_metadata import ProviderMetadata
from mfdballm.types import ProviderResponse


class BaseProvider:
    """
    Base class for all providers.
    """

    def __init__(self, name: str | None = None):
        self._name = name or self.__class__.__name__

    @property
    def metadata(self) -> ProviderMetadata:
        """
        Default provider metadata.
        """
        return ProviderMetadata(
            name=self._name,
            supports_tools=False,
            supports_stream=False,
        )

    async def generate(self, prompt: str) -> ProviderResponse:
        """
        Execute model request.
        Real providers must override this.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement generate()"
        )
