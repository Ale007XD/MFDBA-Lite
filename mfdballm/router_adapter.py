import inspect

from mfdballm.models.provider_response import ProviderResponse


class RouterAdapter:
    """
    Adapter between ExecutionEngine and Router.

    Guarantees:
        call(...) -> ProviderResponse
    """

    def __init__(self, router):
        self.router = router

    async def call(self, messages, tools=None) -> ProviderResponse:

        if not hasattr(self.router, "chat") and not hasattr(self.router, "achat"):
            raise RuntimeError("Router must implement chat() or achat()")

        # prefer async router
        if hasattr(self.router, "achat"):
            fn = self.router.achat
        else:
            fn = self.router.chat

        sig = inspect.signature(fn)

        if "tools" in sig.parameters:
            result = fn(messages, tools=tools)
        else:
            result = fn(messages)

        if inspect.isawaitable(result):
            result = await result

        # Router returns string → wrap
        if isinstance(result, str):
            return ProviderResponse(text=result)

        # Router may return ProviderResponse
        if isinstance(result, ProviderResponse):
            return result

        # dict fallback
        if isinstance(result, dict):
            return ProviderResponse.normalize(result)

        raise TypeError(
            f"Unsupported router response type: {type(result)}"
        )
