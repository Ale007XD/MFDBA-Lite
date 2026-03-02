# mfdballm/router.py

import logging
import time
from typing import List, Dict

from mfdballm.providers.base import BaseProvider
from mfdballm.exceptions import (
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)

logger = logging.getLogger("mfdballm.router")


class Router:
    """
    Production-grade Router.

    Responsibilities:
    - Deterministic provider order
    - Timeout isolation
    - Exponential backoff retry
    - Provider-level fallback
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        max_retries: int = 3,
        base_backoff: float = 1.0,
    ):
        if not providers:
            raise ValueError("No providers configured")

        self.providers = providers
        self.max_retries = max_retries
        self.base_backoff = base_backoff

    def chat(
        self,
        messages: List[Dict[str, str]],
        timeout: int = 30,
    ) -> str:

        start_time = time.monotonic()
        last_error = None

        provider_count = len(self.providers)
        if provider_count == 0:
            raise RuntimeError("No providers available")

        # Timeout isolation
        per_provider_timeout = max(5, timeout // provider_count)

        for provider in self.providers:

            if not provider.is_healthy():
                logger.warning(f"Skipping unhealthy provider: {provider.name}")
                continue

            logger.info(f"Router trying provider: {provider.name}")

            for attempt in range(1, self.max_retries + 1):

                # Global timeout guard
                elapsed = time.monotonic() - start_time
                if elapsed > timeout:
                    raise RuntimeError("Global router timeout exceeded")

                try:
                    return provider.chat(
                        messages,
                        timeout=per_provider_timeout,
                    )

                except (
                    ProviderRateLimitError,
                    ProviderTimeoutError,
                    ProviderUnavailableError,
                ) as e:

                    last_error = e

                    logger.warning(
                        f"{provider.name} attempt {attempt}/{self.max_retries} failed: {e}"
                    )

                    if attempt >= self.max_retries:
                        logger.warning(
                            f"{provider.name} exhausted retries, moving to next provider"
                        )
                        break

                    # Exponential backoff
                    backoff_time = self.base_backoff * (2 ** (attempt - 1))

                    logger.info(
                        f"{provider.name} backoff sleeping {backoff_time:.1f}s"
                    )

                    time.sleep(backoff_time)

                except Exception as e:
                    # Non-retryable error
                    logger.error(f"{provider.name} unexpected error: {e}")
                    last_error = e
                    break

        raise RuntimeError(f"All providers failed. Last error: {last_error}")
