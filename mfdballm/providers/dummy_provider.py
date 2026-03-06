from mfdballm.providers.base_provider import BaseProvider
from mfdballm.types import ProviderResponse
from mfdballm.types_provider_metadata import ProviderMetadata


class DummyProvider(BaseProvider):

    def __init__(self, name, api_key, model):
        self._name = name
        self._api_key = api_key
        self._model = model

    @property
    def metadata(self) -> ProviderMetadata:
        return ProviderMetadata(
            name=self._name,
            models=[self._model],
            supports_tools=True,
            supports_stream=False,
            max_context_tokens=4096
        )

    async def generate(self, prompt: str) -> ProviderResponse:
        return ProviderResponse(
            text="Hello from DummyProvider!"
        )
