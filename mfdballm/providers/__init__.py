# mfdballm/providers/__init__.py

"""
Providers package.

Providers are exposed via lazy import to avoid importing
optional dependencies unless they are actually used.
"""

from importlib import import_module
from typing import Any

__all__ = [
    "OpenRouterProvider",
    "GeminiProvider",
    "GroqProvider",
]


def __getattr__(name: str) -> Any:
    if name == "OpenRouterProvider":
        return import_module(".openrouter_provider", __name__).OpenRouterProvider

    if name == "GeminiProvider":
        return import_module(".gemini_provider", __name__).GeminiProvider

    if name == "GroqProvider":
        return import_module(".groq_provider", __name__).GroqProvider

    raise AttributeError(f"module {__name__} has no attribute {name}")
