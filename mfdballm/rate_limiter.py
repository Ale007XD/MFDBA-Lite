import time
import logging
from collections import deque

logger = logging.getLogger("mfdballm.rate_limiter")


class RateLimiter:
    def __init__(self, max_requests=10, window_seconds=60, min_delay=5):
        self.max_requests = max_requests
        self.window = window_seconds
        self.min_delay = min_delay

        self.requests = deque()
        self.last_request_time = 0

        self.cooldown_until = 0
        self.cooldown_active = False

    def wait_if_needed(self, max_sleep_cap=15):
        now = time.time()

        if now < self.cooldown_until:
            sleep_time = min(self.cooldown_until - now, max_sleep_cap)
            if sleep_time > 0:
                logger.warning(f"Cooldown active: sleeping {int(sleep_time)}s")
                time.sleep(sleep_time)

        while self.requests and now - self.requests[0] > self.window:
            self.requests.popleft()

        if len(self.requests) >= self.max_requests:
            sleep_time = self.window - (now - self.requests[0])
            sleep_time = min(sleep_time, max_sleep_cap)
            if sleep_time > 0:
                logger.warning(f"Window limit reached: sleeping {int(sleep_time)}s")
                time.sleep(sleep_time)

        now = time.time()
        delta = now - self.last_request_time
        if delta < self.min_delay:
            sleep_time = min(self.min_delay - delta, max_sleep_cap)
            if sleep_time > 0:
                logger.debug(f"Min delay: sleeping {int(sleep_time)}s")
                time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.requests.append(self.last_request_time)

    def trigger_cooldown(self, seconds=30):
        now = time.time()
        if not self.cooldown_active or now > self.cooldown_until:
            self.cooldown_until = now + seconds
            self.cooldown_active = True
            logger.warning(f"Cooldown triggered for {seconds}s")
