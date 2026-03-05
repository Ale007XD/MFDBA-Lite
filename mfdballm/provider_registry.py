from mfdballm.providers.groq_provider import GroqProvider
from mfdballm.providers.gemini_provider import GeminiProvider
from mfdballm.providers.openrouter_provider import OpenRouterProvider


def build_providers(config):

    providers = []

    providers_config = config.get("providers", {})

    for name, p in providers_config.items():

        if not p.get("enabled", True):
            continue

        if name == "groq":

            providers.append(
                GroqProvider(
                    api_key=p["api_key"],
                    model=p["model"]
                )
            )

        elif name == "gemini":

            providers.append(
                GeminiProvider(
                    api_key=p["api_key"],
                    model=p["model"]
                )
            )

        elif name == "openrouter":

            providers.append(
                OpenRouterProvider(
                    api_key=p["api_key"],
                    model=p["model"]
                )
            )

    return providers
