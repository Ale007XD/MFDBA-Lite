import os


class ProviderRegistry:
    """
    Registry for all LLM providers.

    Responsibilities:
    - load providers from environment
    - store provider instances
    - provide access for Router
    """

    def __init__(self):
        self.providers = {}

    # ---------------------------------------------------------
    # basic registry operations
    # ---------------------------------------------------------

    def register(self, name, provider):
        """
        Register provider instance.
        """
        self.providers[name] = provider

    def get(self, name):
        """
        Get provider by name.
        """
        return self.providers.get(name)

    def list(self):
        """
        List provider names.
        """
        return list(self.providers.keys())

    def get_providers(self):
        """
        Return provider instances (used by Router).
        """
        return list(self.providers.values())

    # ---------------------------------------------------------
    # environment loader
    # ---------------------------------------------------------

    def load_from_env(self):
        """
        Auto-load providers based on available API keys.
        """

        # OpenRouter
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            from mfdballm.providers.openrouter_provider import OpenRouterProvider

            provider = OpenRouterProvider(api_key=openrouter_key)
            self.register("openrouter", provider)

        # Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            from mfdballm.providers.groq_provider import GroqProvider

            provider = GroqProvider(api_key=groq_key)
            self.register("groq", provider)

        # Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            from mfdballm.providers.gemini_provider import GeminiProvider

            provider = GeminiProvider(api_key=gemini_key)
            self.register("gemini", provider)
