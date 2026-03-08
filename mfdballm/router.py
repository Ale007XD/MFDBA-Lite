import asyncio
import inspect
import time
import threading

from enum import Enum
from typing import List, Any, Optional

from mfdballm.models.provider_response import ProviderResponse


class CircuitState(Enum):

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class ProviderState:

    def __init__(self, provider, reset_timeout: int):

        self.provider = provider
        self.reset_timeout = reset_timeout

        self.failures = 0
        self.state = CircuitState.CLOSED
        self.opened_at: Optional[float] = None

        self._lock = threading.Lock()

    # ------------------------------------------------

    def is_available(self):

        with self._lock:

            if self.state == CircuitState.CLOSED:
                return True

            if self.state == CircuitState.OPEN:

                if self.opened_at is None:
                    return False

                if time.time() - self.opened_at >= self.reset_timeout:
                    self.state = CircuitState.HALF_OPEN
                    return True

                return False

            if self.state == CircuitState.HALF_OPEN:
                return True

            return False

    # ------------------------------------------------

    def record_failure(self, threshold: int):

        with self._lock:

            if self.state == CircuitState.HALF_OPEN:

                self.state = CircuitState.OPEN
                self.opened_at = time.time()
                self.failures = threshold
                return

            self.failures += 1

            if self.failures >= threshold:
                self.state = CircuitState.OPEN
                self.opened_at = time.time()

    # ------------------------------------------------

    def record_success(self):

        with self._lock:

            self.failures = 0
            self.state = CircuitState.CLOSED
            self.opened_at = None


class Router:

    FAILURE_THRESHOLD = 2
    RESET_TIMEOUT = 1

    def __init__(self, providers: List[Any]):

        if not providers:
            raise ValueError("Router requires providers")

        self.providers = providers

        self._states = [
            ProviderState(p, self.RESET_TIMEOUT)
            for p in providers
        ]

        self._provider_supports_tools = {}

    # ------------------------------------------------

    @property
    def provider_states(self):
        return self._states

    # ------------------------------------------------

    def get_health_snapshot(self):

        snapshot = []

        for state in self._states:

            snapshot.append(
                {
                    "provider": state.provider.__class__.__name__,
                    "state": state.state.value,
                    "failures": state.failures
                }
            )

        return snapshot

    # ------------------------------------------------

    def _supports_tools(self, provider):

        key = provider.__class__

        if key not in self._provider_supports_tools:

            sig = inspect.signature(provider.chat)
            self._provider_supports_tools[key] = "tools" in sig.parameters

        return self._provider_supports_tools[key]

    # ------------------------------------------------
    # PUBLIC SYNC API
    # ------------------------------------------------

    def chat(self, messages, tools=None, timeout=None):
        """
        Sync entrypoint.

        Returns:
            str
        """

        async def runner():
            resp = await self._chat(messages, tools, timeout)
            return resp.text

        try:
            asyncio.get_running_loop()
            return runner()
        except RuntimeError:
            return asyncio.run(runner())

    # ------------------------------------------------
    # ASYNC API (used by runtime)
    # ------------------------------------------------

    async def achat(self, messages, tools=None, timeout=None):
        """
        Async entrypoint.

        Returns:
            ProviderResponse
        """

        return await self._chat(messages, tools, timeout)

    # ------------------------------------------------
    # CORE ROUTER
    # ------------------------------------------------

    async def _chat(self, messages, tools=None, timeout=None):

        last_error = None

        for state in self._states:

            if not state.is_available():
                continue

            provider = state.provider

            try:

                # -----------------------------
                # call provider
                # -----------------------------

                if self._supports_tools(provider):
                    result = provider.chat(messages, tools=tools)
                else:
                    result = provider.chat(messages)

                # async provider
                if inspect.isawaitable(result):

                    if timeout:
                        result = await asyncio.wait_for(result, timeout)
                    else:
                        result = await result

                # sync provider
                elif timeout:
                    result = await asyncio.wait_for(
                        asyncio.to_thread(lambda: result),
                        timeout
                    )

                if result is None:
                    raise RuntimeError("Provider returned None")

                response = ProviderResponse.normalize(result)

                state.record_success()

                return response

            except asyncio.TimeoutError as e:

                last_error = e

                # timeout НЕ должен trip circuit
                continue

            except asyncio.CancelledError:
                raise

            except Exception as e:

                last_error = e
                state.record_failure(self.FAILURE_THRESHOLD)

        raise RuntimeError(
            f"All providers failed. Last error: {last_error}"
        )
