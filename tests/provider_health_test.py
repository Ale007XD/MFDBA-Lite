from mfdballm.providers.provider_health import ProviderHealth


def main():

    h = ProviderHealth()

    h.record_success(100)
    h.record_success(200)
    h.record_failure()

    assert h.calls == 3

    assert h.avg_latency == 100

    assert h.failures == 1

    print("PROVIDER HEALTH TEST PASSED")


if __name__ == "__main__":
    main()
