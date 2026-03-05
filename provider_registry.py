from mfdballm.providers.gemini_provider import GeminiProvider
from mfdballm.providers.groq_provider import GroqProvider
from mfdballm.providers.openrouter_provider import OpenRouterProvider


def build_providers(config):

    providers = []

    provider_cfg = config["providers"]

    # GEMINI
    if provider_cfg["gemini"]["enabled"]:
        providers.append(
            GeminiProvider(provider_cfg["gemini"])
        )

    # GROQ
    if provider_cfg["groq"]["enabled"]:
        providers.append(
            GroqProvider(provider_cfg["groq"])
        )

    # OPENROUTER
    if provider_cfg["openrouter"]["enabled"]:
        providers.append(
            OpenRouterProvider(provider_cfg["openrouter"])
        )

    return providers
