from mfdballm.config_loader import load_config


def test_load_config():
    """
    Basic test to ensure configuration loads without errors.
    """
    config = load_config()

    assert config is not None


def test_config_structure():
    """
    Optional sanity check for config structure.
    """
    config = load_config()

    # config может быть dict или объектом
    assert isinstance(config, dict) or hasattr(config, "__dict__")
