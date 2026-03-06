from mfdballm.providers.provider_runtime_manager import ProviderRuntimeManager
from mfdballm.providers.dummy_provider import DummyProvider


def main():

    manager = ProviderRuntimeManager()

    p = DummyProvider("dummy", "key", "model")

    manager.register(p)

    providers = manager.available_providers()

    assert len(providers) == 1

    print("PROVIDER RUNTIME MANAGER TEST PASSED")


if __name__ == "__main__":
    main()
