class ProviderHealth:

    def __init__(self):

        self.failures = 0
        self.successes = 0
        self.total_latency_ms = 0
        self.calls = 0

    def record_success(self, latency_ms):

        self.successes += 1
        self.calls += 1
        self.total_latency_ms += latency_ms

    def record_failure(self):

        self.failures += 1
        self.calls += 1

    @property
    def avg_latency(self):

        if self.calls == 0:
            return 0

        return int(self.total_latency_ms / self.calls)

    @property
    def failure_rate(self):

        if self.calls == 0:
            return 0

        return self.failures / self.calls
