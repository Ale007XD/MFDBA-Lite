import asyncio
import time
import inspect
from typing import List, Any, Optional
from mfdballm.types import ProviderResponse


class Router:
    """
    Fallback router with circuit breaker.

    - sync + async compatible
    - provider signature adaptive
    - health snapshot support
    """

    FAILURE_THRESHOLD = 2
    RESET_TIMEOUT = 30

    def __init__(self, providers: List[Any]):
        if not providers:
            raise ValueError("Router requires at least one provider")

        self.providers = providers

        self._state = [
            {
                "provider": p,
                "failures": 0,
                "circuit_open": False,
                "opened_at": None,
            }
            for p in providers
        ]

    # --------------------------------------------------
    # ENTRYPOINT
    # --------------------------------------------------

    def chat(self, messages, tools=None):

        try:
            asyncio.get_running_loop()
            return self._chat(messages, tools)
        except RuntimeError:
            return asyncio.run(self._chat(messages, tools))

    # --------------------------------------------------

    async def _chat(self, messages, tools=None) -> ProviderResponse:

        last_error: Optional[Exception] = None

        for entry in self._state:

            provider = entry["provider"]

            # circuit breaker
            if entry["circuit_open"]:
                if time.time() - entry["opened_at"] < self.RESET_TIMEOUT:
                    continue
                else:
                    entry["circuit_open"] = False
                    entry["failures"] = 0

            try:

                if not hasattr(provider, "chat"):
                    raise AttributeError(
                        f"{provider.__class__.__name__} has no chat() method"
                    )

                # --------------------------------------------------
                # ADAPT TO PROVIDER SIGNATURE
                # --------------------------------------------------

                sig = inspect.signature(provider.chat)

                if "tools" in sig.parameters:
                    result = await provider.chat(messages, tools=tools)
                else:
                    result = await provider.chat(messages)

                entry["failures"] = 0

                if result is None:
                    raise RuntimeError(
                        f"{provider.__class__.__name__} returned None"
                    )

                return result

            except Exception as e:

                last_error = e
                entry["failures"] += 1

                if entry["failures"] >= self.FAILURE_THRESHOLD:
                    entry["circuit_open"] = True
                    entry["opened_at"] = time.time()

        raise RuntimeError(f"All providers failed. Last error: {last_error}")

    # --------------------------------------------------
    # HEALTH SNAPSHOT
    # --------------------------------------------------

    def get_health_snapshot(self):

        snapshot = []

        for entry in self._state:

            state = "OPEN" if entry["circuit_open"] else "CLOSED"

            snapshot.append(
                {
                    "provider": entry["provider"].__class__.__name__,
                    "state": state,
                    "failures": entry["failures"],
                }
            )

        return snapshot
