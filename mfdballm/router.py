import time
import random
from enum import Enum

from .config import config


class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class ProviderState:

    def __init__(self, provider):
        self.provider = provider
        self.state = CircuitState.CLOSED

        self.success_count = 0
        self.failure_count = 0
        self.consecutive_failures = 0

        self.opened_at = None
        self.half_open_successes = 0

        self.ema_latency = None


    def _update_latency(self, latency):

        alpha = 0.2

        if self.ema_latency is None:
            self.ema_latency = latency
        else:
            self.ema_latency = (alpha * latency) + ((1 - alpha) * self.ema_latency)


    def is_available(self):

        now = time.time()

        if self.state == CircuitState.OPEN:

            if self.opened_at is None:
                return False

            if now >= self.opened_at + config.RECOVERY_TIMEOUT:
                self.state = CircuitState.HALF_OPEN
                self.half_open_successes = 0
            else:
                return False

        return True


    def record_success(self, latency):

        self.success_count += 1
        self.consecutive_failures = 0

        self._update_latency(latency)

        if self.state == CircuitState.HALF_OPEN:

            self.half_open_successes += 1

            if self.half_open_successes >= config.HALF_OPEN_MAX_REQUESTS:
                self.state = CircuitState.CLOSED
                self.half_open_successes = 0


    def record_failure(self):

        self.failure_count += 1
        self.consecutive_failures += 1

        if self.state == CircuitState.HALF_OPEN:
            self._trip()

        elif (
            self.state == CircuitState.CLOSED
            and self.consecutive_failures >= config.FAILURE_THRESHOLD
        ):
            self._trip()


    def _trip(self):

        self.state = CircuitState.OPEN
        self.opened_at = time.time()
        self.half_open_successes = 0


    def health_score(self):

        success = self.success_count
        fail = self.failure_count

        total = success + fail

        if total == 0:
            reliability = 0.5
        else:
            reliability = success / total

        latency_factor = 1.0

        if self.ema_latency:
            latency_factor = 1 / (1 + self.ema_latency)

        return round(reliability * latency_factor, 3)


    def snapshot(self):

        return {
            "provider": self.provider.name,
            "state": self.state.value,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "consecutive_failures": self.consecutive_failures,
            "ema_latency": self.ema_latency,
            "health_score": self.health_score(),
        }


class Router:

    def __init__(self, providers):

        self.states = [ProviderState(p) for p in providers]


    def chat(self, messages):

        last_error = None

        for attempt in range(config.MAX_RETRIES):

            available = [
                s for s in self.states
                if s.is_available()
            ]

            if not available:
                raise Exception("No healthy providers available")

            state = random.choice(available)

            start = time.time()

            try:

                result = state.provider.chat(messages)

                latency = time.time() - start

                state.record_success(latency)

                return result

            except Exception as e:

                state.record_failure()

                last_error = e

                time.sleep(config.BASE_BACKOFF)

        raise Exception(f"All providers failed. Last error: {last_error}")


    def get_health_snapshot(self):

        return [s.snapshot() for s in self.states]
