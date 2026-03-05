import os

from mfdballm.config_loader import load_config

from mfdballm.providers.gemini import GeminiProvider
from mfdballm.providers.groq import GroqProvider
from mfdballm.providers.openai_compat import OpenAICompatProvider


def build_providers():
    """
    Build provider instances based on config and API keys.
    """

    config = load_config()

    providers = []

    providers_cfg = config.get("providers", {})
    router_cfg = config.get("router", {})

    order = router_cfg.get("order", ["groq", "gemini", "openrouter"])

    for name in order:

        if name == "groq":
            cfg = providers_cfg.get("groq", {})

            api_key = os.getenv("GROQ_API_KEY") or cfg.get("api_key")

            if api_key:
                providers.append(
                    GroqProvider(
                        api_key=api_key
                    )
                )

        elif name == "gemini":
            cfg = providers_cfg.get("gemini", {})

            api_key = os.getenv("GEMINI_API_KEY") or cfg.get("api_key")

            if api_key:
                providers.append(
                    GeminiProvider(
                        api_key=api_key
                    )
                )

        elif name == "openrouter":
            cfg = providers_cfg.get("openrouter", {})

            api_key = os.getenv("OPENROUTER_API_KEY") or cfg.get("api_key")

            if api_key:
                providers.append(
                    OpenAICompatProvider(
                        api_key=api_key,
                        base_url="https://openrouter.ai/api/v1"
                    )
                )

    if not providers:
        raise RuntimeError(
            "No providers available. Set API keys."
        )

    return providers
