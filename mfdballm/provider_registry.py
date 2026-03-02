# mfdballm/provider_registry.py

import os
from typing import List

from mfdballm.providers.groq import GroqProvider
from mfdballm.providers.openrouter import OpenRouterProvider


def build_providers() -> List:
    """
    Build providers in deterministic priority order.

    Order:
        1. Groq
        2. OpenRouter
    """

    providers = []

    try:
        providers.append(GroqProvider())
    except Exception:
        pass

    try:
        providers.append(OpenRouterProvider())
    except Exception:
        pass

    if not providers:
        raise RuntimeError("No providers available")

    return providers
