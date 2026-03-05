from .providers.groq_provider import GroqProvider
from .providers.gemini_provider import GeminiProvider
from .providers.openrouter_provider import OpenRouterProvider


def build_providers(config):

    providers = []

    provider_cfg = config["providers"]

    # GROQ
    if provider_cfg["groq"]["enabled"]:
        providers.append(
            GroqProvider(
                api_key=provider_cfg["groq"]["api_key"],
                model=provider_cfg["groq"]["model"]
            )
        )

    # GEMINI
    if provider_cfg["gemini"]["enabled"]:
        providers.append(
            GeminiProvider(
                provider_cfg["gemini"]
            )
        )

    # OPENROUTER
    if provider_cfg["openrouter"]["enabled"]:
        providers.append(
            OpenRouterProvider(
                provider_cfg["openrouter"]
            )
        )

    return providers
