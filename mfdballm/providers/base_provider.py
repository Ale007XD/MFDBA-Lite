from abc import ABC
from typing import List, Dict, Any, Optional
import time
import inspect

from mfdballm.types_provider_metadata import ProviderMetadata
from mfdballm.models.provider_response import ProviderResponse


class BaseProvider(ABC):
    """
    Abstract base class for all LLM providers.

    Contract:
        async chat(messages, tools) -> ProviderResponse
    """

    HEALTH_CACHE_TTL = 2  # seconds

    def __init__(self, name: Optional[str] = None):

        self._name = name or self.__class__.__name__

        # health cache
        self._health_cached: Optional[bool] = None
        self._health_checked_at: Optional[float] = None

    # --------------------------------------------------
    # METADATA
    # --------------------------------------------------

    @property
    def metadata(self) -> ProviderMetadata:
        """
        Default provider metadata.
        Providers may override this.
        """
        return ProviderMetadata(
            name=self._name,
            supports_tools=False,
            supports_stream=False,
        )

    # --------------------------------------------------
    # HEALTH CHECK
    # --------------------------------------------------

    def is_healthy(self) -> bool:
        """
        Provider health check with cache.

        Default behavior:
            - If provider implements `health()`, use it.
            - Otherwise assume provider is healthy.

        Health checks are cached to avoid expensive calls.

        IMPORTANT:
        health() must be synchronous.
        Async health checks are intentionally ignored to
        prevent event loop misuse.
        """

        now = time.time()

        # cached result
        if (
            self._health_cached is not None
            and self._health_checked_at
            and now - self._health_checked_at < self.HEALTH_CACHE_TTL
        ):
            return self._health_cached

        try:

            if hasattr(self, "health"):

                result = self.health()

                # Prevent asyncio misuse inside sync Router code
                if inspect.isawaitable(result):
                    raise RuntimeError(
                        f"{self.__class__.__name__}.health() must be synchronous"
                    )

                healthy = bool(result)

            else:

                healthy = True

        except Exception:

            healthy = False

        self._health_cached = healthy
        self._health_checked_at = now

        return healthy

    # --------------------------------------------------
    # MAIN CONTRACT
    # --------------------------------------------------

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[list] = None,
    ) -> ProviderResponse:
        """
        Execute a chat completion request.

        Default adapter for legacy providers.

        Providers may implement either:
            - chat(...)
            - complete(...)

        messages:
            [
                {"role": "system", "content": "..."},
                {"role": "user", "content": "..."}
            ]

        tools:
            Optional tool schema list.
        """

        if hasattr(self, "complete"):
            return await self.complete(messages, tools=tools)

        raise NotImplementedError(
            f"{self.__class__.__name__} must implement chat() or complete()"
        )
