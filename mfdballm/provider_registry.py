# mfdballm/provider_registry.py

from typing import List, Type

from mfdballm.config import get_provider_order
from mfdballm.providers.base import BaseProvider
from mfdballm.providers.groq import GroqProvider
from mfdballm.providers.openrouter import OpenRouterProvider
from mfdballm.providers.gemini import GeminiProvider


PROVIDER_MAP: dict[str, Type[BaseProvider]] = {
    "groq": GroqProvider,
    "openrouter": OpenRouterProvider,
    "gemini": GeminiProvider,
}


def build_providers() -> List[BaseProvider]:
    """
    Deterministic provider builder.

    Order resolution:
        1. MFDBA_PROVIDER_ORDER env
        2. DEFAULT_PROVIDER_ORDER from config

    Providers that fail to initialize
    (e.g. missing API key) are skipped.

    Raises:
        RuntimeError if no providers available.
    """

    order = get_provider_order()

    providers: List[BaseProvider] = []

    for name in order:
        provider_cls = PROVIDER_MAP.get(name.lower())
        if not provider_cls:
            continue

        try:
            providers.append(provider_cls())
        except Exception:
            # Missing API key or other initialization failure
            continue

    if not providers:
        raise RuntimeError(
            "No providers available after deterministic build"
        )

    return providers
