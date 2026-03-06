class ProviderPool:

    def __init__(self, runtime_manager):

        self.runtime_manager = runtime_manager

    def load(self, providers):

        for provider in providers:

            self.runtime_manager.register(provider)

    def list(self):

        return list(self.runtime_manager.providers.values())
