import unittest
import time

from mfdballm.providers.base import BaseProvider


class CountingProvider(BaseProvider):
    def __init__(self):
        super().__init__("counter")
        self.counter = 0

    def chat(self, messages):
        return "OK"

    def health(self):
        self.counter += 1
        return True


class HealthCacheTest(unittest.TestCase):

    def test_health_cached(self):
        provider = CountingProvider()

        provider.is_healthy()
        provider.is_healthy()

        self.assertEqual(provider.counter, 1)


if __name__ == "__main__":
    unittest.main()
