from mfdballm.providers.provider_capabilities import ProviderCapabilities


def main():

    c = ProviderCapabilities()

    assert c.supports_tools

    print("PROVIDER CAPABILITIES TEST PASSED")


if __name__ == "__main__":

    main()
