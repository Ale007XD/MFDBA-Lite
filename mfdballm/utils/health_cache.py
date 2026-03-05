import time

class HealthCache:

    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}

    def healthy(self, provider):

        now = time.time()

        if provider not in self.cache:
            return True

        return now - self.cache[provider] > self.ttl
