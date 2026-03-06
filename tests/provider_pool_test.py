from mfdballm.providers.provider_pool import ProviderPool
from mfdballm.providers.provider_runtime_manager import ProviderRuntimeManager
from mfdballm.providers.dummy_provider import DummyProvider


def main():

    manager = ProviderRuntimeManager()

    pool = ProviderPool(manager)

    p = DummyProvider("dummy", "key", "model")

    pool.load([p])

    providers = pool.list()

    assert len(providers) == 1

    print("PROVIDER POOL TEST PASSED")


if __name__ == "__main__":
    main()
