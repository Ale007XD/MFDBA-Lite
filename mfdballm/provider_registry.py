import os

from mfdballm.providers.gemini_provider import GeminiProvider
from mfdballm.providers.groq_provider import GroqProvider
from mfdballm.providers.openrouter_provider import OpenRouterProvider


def build_providers():
    providers = []

    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")

    if groq_key:
        providers.append(
            GroqProvider(
                api_key=groq_key,
                model="llama3-70b-8192"
            )
        )

    if gemini_key:
        providers.append(
            GeminiProvider(
                api_key=gemini_key,
                model="gemini-2.0-flash"
            )
        )

    if openrouter_key:
        providers.append(
            OpenRouterProvider(
                api_key=openrouter_key,
                model="openai/gpt-4o-mini"
            )
        )

    if not providers:
        raise RuntimeError("No providers available. Set API keys.")

    return providers
