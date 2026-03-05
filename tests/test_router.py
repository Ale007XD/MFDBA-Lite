import unittest
import time

from mfdballm.router import Router
from mfdballm.providers.base import BaseProvider


class HealthyProvider(BaseProvider):
    def __init__(self):
        super().__init__("healthy")

    def chat(self, messages, timeout=None):
        return "OK"

    def health(self):
        return True


class FailingProvider(BaseProvider):
    def __init__(self):
        super().__init__("failing")

    def chat(self, messages, timeout=None):
        raise RuntimeError("Failure")

    def health(self):
        return True


class RouterTest(unittest.TestCase):

    def test_fallback(self):
        router = Router([FailingProvider(), HealthyProvider()])
        result = router.chat([{"role": "user", "content": "hi"}])
        self.assertEqual(result, "OK")

    def test_all_fail(self):
        router = Router([FailingProvider()])
        with self.assertRaises(RuntimeError):
            router.chat([{"role": "user", "content": "hi"}])

    def test_circuit_opens(self):
        router = Router([FailingProvider()])
        for _ in range(3):
            try:
                router.chat([{"role": "user", "content": "hi"}])
            except RuntimeError:
                pass

        snapshot = router.get_health_snapshot()[0]
        self.assertEqual(snapshot["state"], "OPEN")


if __name__ == "__main__":
    unittest.main()
