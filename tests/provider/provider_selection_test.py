from mfdballm.providers.provider_runtime_manager import ProviderRuntimeManager
from mfdballm.providers.dummy_provider import DummyProvider


def main():

    manager = ProviderRuntimeManager()

    p = DummyProvider("dummy", "key", "model")

    manager.register(p)

    selected = manager.select_provider()

    assert selected.metadata.name == "dummy"

    print("PROVIDER SELECTION TEST PASSED")


if __name__ == "__main__":
    main()
