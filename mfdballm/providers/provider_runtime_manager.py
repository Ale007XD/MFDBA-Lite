from mfdballm.providers.provider_health_registry import ProviderHealthRegistry
from mfdballm.providers.provider_selection_strategy import ProviderSelectionStrategy


class ProviderRuntimeManager:

    def __init__(self):

        self.providers = {}

        self.health_registry = ProviderHealthRegistry()

        self.selection_strategy = ProviderSelectionStrategy()

    def register(self, provider):

        name = provider.metadata.name

        self.providers[name] = provider

    def get(self, name):

        return self.providers[name]

    def health(self, name):

        return self.health_registry.get(name)

    def available_providers(self):

        result = []

        for name in self.providers:

            health = self.health_registry.get(name)

            if health.failure_rate < 0.5:

                result.append(self.providers[name])

        return result

    def select_provider(self):

        providers = self.available_providers()

        if not providers:

            raise RuntimeError("No providers available")

        return self.selection_strategy.select(
            providers,
            self.health_registry
        )
