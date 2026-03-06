class ProviderHealthRegistry:

    def __init__(self):

        self.providers = {}

    def get(self, provider_name):

        if provider_name not in self.providers:

            from mfdballm.providers.provider_health import ProviderHealth

            self.providers[provider_name] = ProviderHealth()

        return self.providers[provider_name]
