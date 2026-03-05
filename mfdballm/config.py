# mfdballm/config.py


class Config:

    def __init__(self):

        # Router provider order
        self.PROVIDERS = [
            "gemini",
            "openrouter",
            "local",
        ]

        # Gemini (free tier)
        self.GEMINI_MODELS = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-pro",
        ]

        # OpenRouter free models
        self.OPENROUTER_MODELS = [
            "mistralai/mistral-7b-instruct",
            "meta-llama/llama-3-8b-instruct",
        ]

        # Local models
        self.LOCAL_MODELS = [
            "llama3",
            "mistral",
        ]

        # Router retry
        self.MAX_RETRIES = 2

        # Circuit breaker
        self.FAILURE_THRESHOLD = 3
        self.RESET_TIMEOUT = 30

        # Retry backoff
        self.BASE_BACKOFF = 1.5

        # Request timeout
        self.REQUEST_TIMEOUT = 60


config = Config()


# -------------------------
# Provider order
# -------------------------

def get_provider_order():
    return config.PROVIDERS


# -------------------------
# Gemini
# -------------------------

def get_gemini_models():
    return config.GEMINI_MODELS


def get_gemini_model():
    return config.GEMINI_MODELS[0]


# -------------------------
# OpenRouter
# -------------------------

def get_openrouter_models():
    return config.OPENROUTER_MODELS


def get_openrouter_model():
    return config.OPENROUTER_MODELS[0]


# -------------------------
# Local models
# -------------------------

def get_local_models():
    return config.LOCAL_MODELS


def get_local_model():
    return config.LOCAL_MODELS[0]
