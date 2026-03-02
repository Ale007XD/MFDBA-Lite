from mfdballm.providers.groq import GroqProvider
from mfdballm.providers.openrouter import OpenRouterProvider
from mfdballm.providers.gemini import GeminiProvider


def build_providers():
    """
    Return providers in priority order.
    Order matters for router fallback.
    """

    return [
        OpenRouterProvider(),
        GroqProvider(),
        GeminiProvider(),
    ]
