# mfdballm/router.py

import logging
import time
from typing import List, Dict, Any

from mfdballm.providers.base import BaseProvider
from mfdballm.exceptions import (
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)

logger = logging.getLogger("mfdballm.router")


class ProviderState:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

        self.success_count = 0
        self.failure_count = 0
        self.consecutive_failures = 0

        self.ema_latency = None
        self.cooldown_until = 0

    @property
    def health_score(self) -> float:
        total = self.success_count + self.failure_count + 1
        success_rate = self.success_count / total

        if self.ema_latency is None:
            latency_factor = 1.0
        else:
            latency_factor = 1 / (1 + self.ema_latency)

        return success_rate * latency_factor

    def record_success(self, latency: float):
        self.success_count += 1
        self.consecutive_failures = 0

        if self.ema_latency is None:
            self.ema_latency = latency
        else:
            alpha = 0.3
            self.ema_latency = alpha * latency + (1 - alpha) * self.ema_latency

    def record_failure(self):
        self.failure_count += 1
        self.consecutive_failures += 1

        if self.consecutive_failures >= 3:
            self.cooldown_until = time.time() + 30

    def is_available(self) -> bool:
        return time.time() >= self.cooldown_until

    def snapshot(self) -> Dict[str, Any]:
        return {
            "provider": self.provider.name,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "consecutive_failures": self.consecutive_failures,
            "ema_latency": self.ema_latency,
            "health_score": round(self.health_score, 3),
            "cooldown_active": not self.is_available(),
            "cooldown_remaining": max(
                0,
                round(self.cooldown_until - time.time(), 1),
            )
            if not self.is_available()
            else 0,
        }


class Router:
    """
    v0.5 Self-Healing Router + Doctor Support
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        max_retries: int = 3,
        base_backoff: float = 1.0,
    ):
        if not providers:
            raise ValueError("No providers configured")

        self.max_retries = max_retries
        self.base_backoff = base_backoff

        self.provider_states = [
            ProviderState(p) for p in providers
        ]

    def _sorted_providers(self):
        return sorted(
            self.provider_states,
            key=lambda s: s.health_score,
            reverse=True,
        )

    def get_health_snapshot(self) -> List[Dict[str, Any]]:
        return [
            state.snapshot()
            for state in self._sorted_providers()
        ]

    def chat(
        self,
        messages: List[Dict[str, str]],
        timeout: int = 30,
    ) -> str:

        start_time = time.monotonic()
        last_error = None

        active_states = [
            s for s in self._sorted_providers()
            if s.is_available() and s.provider.is_healthy()
        ]

        if not active_states:
            raise RuntimeError("No healthy providers available")

        per_provider_timeout = max(5, timeout // len(active_states))

        for state in active_states:

            provider = state.provider

            logger.info(
                f"Router trying provider: {provider.name} "
                f"(score={state.health_score:.3f})"
            )

            for attempt in range(1, self.max_retries + 1):

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
                    state.record_success(latency)

                    logger.info(
                        f"{provider.name} success "
                        f"(latency={latency:.2f}s, "
                        f"score={state.health_score:.3f})"
                    )

                    return result

                except (
                    ProviderRateLimitError,
                    ProviderTimeoutError,
                    ProviderUnavailableError,
                ) as e:

                    state.record_failure()
                    last_error = e

                    logger.warning(
                        f"{provider.name} attempt {attempt}/{self.max_retries} "
                        f"failed: {e}"
                    )

                    if state.cooldown_until > time.time():
                        logger.warning(
                            f"{provider.name} entering cooldown (30s)"
                        )
                        break

                    if attempt >= self.max_retries:
                        logger.warning(
                            f"{provider.name} exhausted retries"
                        )
                        break

                    backoff_time = self.base_backoff * (2 ** (attempt - 1))

                    logger.info(
                        f"{provider.name} backoff sleeping "
                        f"{backoff_time:.1f}s"
                    )

                    time.sleep(backoff_time)

                except Exception as e:
                    state.record_failure()
                    last_error = e
                    logger.error(
                        f"{provider.name} unexpected error: {e}"
                    )
                    break

        raise RuntimeError(
            f"All providers failed. Last error: {last_error}"
        )
