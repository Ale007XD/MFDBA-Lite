class ProviderSelectionStrategy:

    def select(self, providers, health_registry):

        best_provider = None
        best_score = None

        for provider in providers:

            name = provider.metadata.name

            health = health_registry.get(name)

            latency = health.avg_latency

            failure_rate = health.failure_rate

            score = latency + (failure_rate * 1000)

            if best_score is None or score < best_score:

                best_score = score

                best_provider = provider

        return best_provider
