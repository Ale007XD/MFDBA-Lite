from mfdballm.providers.gemini import GeminiProvider
from mfdballm.providers.groq import GroqProvider
from mfdballm.providers.openai_compat import OpenAICompatProvider


def build_providers():
    providers = []

    for cls in [
        GeminiProvider,
        GroqProvider,
        OpenAICompatProvider,
    ]:
        try:
            providers.append(cls())
        except Exception as e:
            print(f"[provider disabled] {cls.__name__}: {e}")

    if not providers:
        raise RuntimeError("No providers available")

    return providers
