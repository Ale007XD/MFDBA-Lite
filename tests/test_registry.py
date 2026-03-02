import unittest
import os

from mfdballm.provider_registry import build_providers


class RegistryTest(unittest.TestCase):

    def setUp(self):
        os.environ["OPENROUTER_API_KEY"] = "test"
        os.environ["MFDBA_PROVIDER_ORDER"] = "openrouter"

    def tearDown(self):
        os.environ.pop("OPENROUTER_API_KEY", None)
        os.environ.pop("MFDBA_PROVIDER_ORDER", None)

    def test_ordering(self):
        providers = build_providers()
        self.assertEqual(providers[0].name, "openrouter")


if __name__ == "__main__":
    unittest.main()
