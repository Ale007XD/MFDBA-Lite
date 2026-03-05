from mfdballm.config_loader import load_config


def main():

    config = load_config()

    print("\nCONFIG LOADED:")
    print(config)


if __name__ == "__main__":
    main()
