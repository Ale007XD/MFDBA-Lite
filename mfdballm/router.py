import logging
from typing import List, Dict

from mfdballm.providers.base import BaseProvider
from mfdballm.exceptions import ProviderRateLimitError, ProviderTimeoutError

logger = logging.getLogger(__name__)


class Router:
    def __init__(self, providers: List[BaseProvider]):
        if not providers:
            raise ValueError("No providers configured")
        self.providers = providers

    def chat(self, messages: List[Dict[str, str]]) -> str:
        last_error = None

        for provider in self.providers:
            if not provider.is_healthy():
                logger.warning(f"Skipping unhealthy provider: {provider.name}")
                continue

            logger.info(f"Router trying provider: {provider.name}")

            try:
                return provider.chat(messages)

            except ProviderRateLimitError as e:
                logger.warning(f"{provider.name} rate limited")
                last_error = e

            except ProviderTimeoutError as e:
                logger.warning(f"{provider.name} timeout")
                last_error = e

            except Exception as e:
                logger.warning(f"{provider.name} failed: {e}")
                last_error = e

        raise RuntimeError(f"All providers failed. Last error: {last_error}")
