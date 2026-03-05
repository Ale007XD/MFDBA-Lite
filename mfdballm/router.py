# mfdballm/router.py

import logging
import time
from enum import Enum
from threading import RLock
from typing import List, Dict, Any

from mfdballm.providers.base import BaseProvider
from mfdballm.config import (
    get_failure_threshold,
    get_recovery_timeout,
    get_half_open_max_requests,
    get_max_retries,
    get_base_backoff,
)
from mfdballm.exceptions import (
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)

logger = logging.getLogger("mfdballm.router")


# ============================================================
# Circuit State
# ============================================================

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


# ============================================================
# Provider State (State Machine Based)
# ============================================================

class ProviderState:

    def __init__(self, provider: BaseProvider):
        self.provider = provider

        self.state = CircuitState.CLOSED

        self.success_count = 0
        self.failure_count = 0
        self.consecutive_failures = 0

        self.opened_at: float | None = None
        self.half_open_successes = 0

        self.ema_latency: float | None = None

    # --------------------------------------------------------

    def _transition_to_open(self):
        self.state = CircuitState.OPEN
        self.opened_at = time.time()
        self.half_open_successes = 0

    def _transition_to_half_open(self):
        self.state = CircuitState.HALF_OPEN
        self.half_open_successes = 0

    def _transition_to_closed(self):
        self.state = CircuitState.CLOSED
        self.consecutive_failures = 0
        self.half_open_successes = 0
        self.opened_at = None

    # --------------------------------------------------------

    def is_available(self) -> bool:
        now = time.time()

        if self.state == CircuitState.OPEN:
            if self.opened_at is None:
                return False

            if now >= self.opened_at + get_recovery_timeout():
                self._transition_to_half_open()
                return True

            return False

        return True

    # --------------------------------------------------------

    def record_success(self, latency: float):
        self.success_count += 1
        self.consecutive_failures = 0

        # EMA update
        if self.ema_latency is None:
            self.ema_latency = latency
        else:
            alpha = 0.3
            self.ema_latency = (
                alpha * latency + (1 - alpha) * self.ema_latency
            )

        if self.state == CircuitState.HALF_OPEN:
            self.half_open_successes += 1
            if (
                self.half_open_successes
                >= get_half_open_max_requests()
            ):
                self._transition_to_closed()

    def record_failure(self):
        self.failure_count += 1
        self.consecutive_failures += 1

        if self.state == CircuitState.HALF_OPEN:
            self._transition_to_open()
            return

        if (
            self.state == CircuitState.CLOSED
            and self.consecutive_failures
            >= get_failure_threshold()
        ):
            self._transition_to_open()

    # --------------------------------------------------------

    @property
    def health_score(self) -> float:
        total = self.success_count + self.failure_count + 1
        success_rate = self.success_count / total

        if self.ema_latency is None:
            latency_factor = 1.0
        else:
            latency_factor = 1 / (1 + self.ema_latency)

        return success_rate * latency_factor

    def snapshot(self) -> Dict[str, Any]:
        return {
            "provider": self.provider.name,
            "state": self.state.value,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "consecutive_failures": self.consecutive_failures,
            "ema_latency": self.ema_latency,
            "health_score": round(self.health_score, 3),
        }


# ============================================================
# Router (Deterministic + Thread Safe)
# ============================================================

class Router:

    def __init__(self, providers: List[BaseProvider]):
        if not providers:
            raise ValueError("No providers configured")

        self._lock = RLock()
        self.provider_states = [
            ProviderState(p) for p in providers
        ]

    # --------------------------------------------------------

    def _sorted_providers(self) -> List[ProviderState]:
        return sorted(
            self.provider_states,
            key=lambda s: s.health_score,
            reverse=True,
        )

    # --------------------------------------------------------

    def get_health_snapshot(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                state.snapshot()
                for state in self._sorted_providers()
            ]

    # --------------------------------------------------------

    def chat(
        self,
        messages: List[Dict[str, str]],
        timeout: int = 30,
    ) -> str:

        start_time = time.monotonic()
        last_error = None

        with self._lock:
            active_states = [
                s for s in self._sorted_providers()
                if s.is_available() and s.provider.is_healthy()
            ]

        if not active_states:
            raise RuntimeError("No healthy providers available")

        per_provider_timeout = max(
            5,
            timeout // max(1, len(active_states)),
        )

        for state in active_states:

            provider = state.provider

            for attempt in range(1, get_max_retries() + 1):

                elapsed = time.monotonic() - start_time
                if elapsed > timeout:
                    raise RuntimeError("Global router timeout exceeded")

                call_start = time.monotonic()

                try:
                    result = provider.chat(
                        messages,
                        timeout=per_provider_timeout,
                    )

                    latency = time.monotonic() - call_start

                    with self._lock:
                        state.record_success(latency)

                    return result

                except (
                    ProviderRateLimitError,
                    ProviderTimeoutError,
                    ProviderUnavailableError,
                ) as e:

                    with self._lock:
                        state.record_failure()

                    last_error = e

                    if attempt >= get_max_retries():
                        break

                    backoff_time = get_base_backoff() * (
                        2 ** (attempt - 1)
                    )
                    time.sleep(backoff_time)

                except Exception as e:

                    with self._lock:
                        state.record_failure()

                    last_error = e
                    break

        raise RuntimeError(
            f"All providers failed. Last error: {last_error}"
        )
