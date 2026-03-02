import time
from collections import deque


class RateLimiter:
    """
    Global IP-safe rate limiter.
    Limits:
    - max_requests per window_seconds
    - minimum delay between requests
    - adaptive cooldown on 429
    """

    def __init__(self, max_requests=10, window_seconds=60, min_delay=5):
        self.max_requests = max_requests
        self.window = window_seconds
        self.min_delay = min_delay
        self.requests = deque()
        self.last_request_time = 0
        self.cooldown_until = 0

    def wait_if_needed(self):
        now = time.time()

        # Cooldown mode
        if now < self.cooldown_until:
            sleep_time = self.cooldown_until - now
            print(f"[COOLDOWN] sleeping {int(sleep_time)}s")
            time.sleep(sleep_time)

        # Remove expired timestamps
        while self.requests and now - self.requests[0] > self.window:
            self.requests.popleft()

        # If too many requests in window → wait
        if len(self.requests) >= self.max_requests:
            sleep_time = self.window - (now - self.requests[0])
            print(f"[WINDOW LIMIT] sleeping {int(sleep_time)}s")
            time.sleep(sleep_time)

        # Enforce minimum delay
        now = time.time()
        if now - self.last_request_time < self.min_delay:
            sleep_time = self.min_delay - (now - self.last_request_time)
            print(f"[MIN DELAY] sleeping {int(sleep_time)}s")
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.requests.append(self.last_request_time)

    def trigger_cooldown(self, seconds=30):
        self.cooldown_until = time.time() + seconds
