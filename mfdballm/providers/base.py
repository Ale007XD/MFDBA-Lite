from abc import ABC, abstractmethod
import time


class BaseProvider(ABC):
    """
    Base class for all providers.
    Supports health caching.
    """

    def __init__(self, name: str):
        self.name = name
        self._health_cache = None
        self._health_cache_time = 0
        self._health_ttl = 5  # seconds

    def is_healthy(self) -> bool:
        """
        Cached health check.
        """
        now = time.time()

        if (
            self._health_cache is not None
            and now - self._health_cache_time < self._health_ttl
        ):
            return self._health_cache

        result = self.health()
        self._health_cache = result
        self._health_cache_time = now
        return result

    @abstractmethod
    def chat(self, messages, timeout=None):
        pass

    @abstractmethod
    def health(self) -> bool:
        pass
