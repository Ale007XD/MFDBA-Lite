from abc import ABC, abstractmethod
import aiohttp


class BaseProvider(ABC):
    """
    Universal base provider for LLM APIs.
    All providers must implement `generate`.
    """

    name = "base"

    def __init__(self, api_key: str, model: str = None, base_url: str = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    @abstractmethod
    async def generate(self, messages, **kwargs):
        """
        Generate response from provider.
        Must return text string.
        """
        raise NotImplementedError()

    async def _post(self, url: str, headers: dict, payload: dict):
        """
        Shared HTTP helper for providers.
        """

        async with aiohttp.ClientSession() as session:

            async with session.post(
                url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:

                if resp.status != 200:
                    text = await resp.text()
                    raise RuntimeError(
                        f"{self.name} API error {resp.status}: {text}"
                    )

                return await resp.json()

    def health(self):
        """
        Basic provider health info.
        """

        return {
            "provider": self.name,
            "model": self.model,
            "base_url": self.base_url,
        }
