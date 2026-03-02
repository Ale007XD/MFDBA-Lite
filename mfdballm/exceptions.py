class ProviderError(Exception):
    """Base provider exception."""
    pass


class ProviderRateLimitError(ProviderError):
    """Provider returned rate limit."""
    pass


class ProviderTimeoutError(ProviderError):
    """Provider request timed out."""
    pass


class ProviderUnavailableError(ProviderError):
    """Provider is unavailable or unhealthy."""
    pass
